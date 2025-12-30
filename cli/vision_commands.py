import typer
import yaml
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ValidationError
from benchmarks.vision.rendering import VisionRenderer, RenderParams, ImageMetadata
from adapters.dummy_vision import DummyVisionAdapter

app = typer.Typer(name="vision", help="SemantIQ-Vision (T2I) Benchmark Commands")
console = Console()

# --- Schema Definition ---

class VisionCategory(BaseModel):
    category_id: str
    name: str
    description: str
    primary_rubrics: List[str]

class VisionRegistry(BaseModel):
    vision_version: str
    benchmark_name: str
    evaluation_scope: str
    supported_output_types: List[str]
    categories: List[VisionCategory]

class VisionArchetype(BaseModel):
    archetype_id: str
    name: str
    description: str
    primary_categories: List[str]
    primary_rubrics: List[str]
    expected_output_properties: List[str]
    allowed_variations: List[str]
    disallowed_patterns: List[str]
    typical_failure_modes: List[str]
    evaluation_notes: Optional[str] = None

class ArchetypeRegistry(BaseModel):
    vision_archetypes_version: str
    archetypes: List[VisionArchetype]

class CategoryArchetypeMapping(BaseModel):
    category_id: str
    primary_archetypes: List[str]
    secondary_archetypes: List[str]
    discouraged_archetypes: List[str]
    rationale: str

class MappingRegistry(BaseModel):
    category_mapping_version: str
    mappings: Dict[str, CategoryArchetypeMapping]

class VisionPrompt(BaseModel):
    prompt_id: str
    category_id: str
    archetype_id: str
    prompt_text: str
    intent: str
    constraints: List[str]
    primary_rubrics: List[str]
    expected_visual_properties: List[str]
    typical_failure_modes: List[str]
    language: str
    version: str

class PromptFile(BaseModel):
    prompts: List[VisionPrompt]

# --- Helpers ---

def load_yaml(path: str) -> Any:
    if not os.path.exists(path):
        console.print(f"[bold red]Error:[/bold red] File not found at {path}")
        raise typer.Exit(code=1)
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            console.print(f"[bold red]Error parsing YAML:[/bold red] {e}")
            raise typer.Exit(code=1)

def load_registry(path: str = "benchmarks/vision/registry.yaml") -> VisionRegistry:
    data = load_yaml(path)
    try:
        registry = VisionRegistry(**data)
        return registry
    except ValidationError as e:
        console.print(f"[bold red]Registry Schema Error:[/bold red]")
        console.print(e)
        raise typer.Exit(code=1)

def load_archetypes(path: str = "benchmarks/vision/prompt_archetypes.yaml") -> ArchetypeRegistry:
    data = load_yaml(path)
    try:
        return ArchetypeRegistry(**data)
    except ValidationError as e:
        console.print(f"[bold red]Archetype Schema Error:[/bold red]")
        console.print(e)
        raise typer.Exit(code=1)

def load_mappings(path: str = "benchmarks/vision/category_archetype_mapping.yaml") -> MappingRegistry:
    data = load_yaml(path)
    try:
        return MappingRegistry(**data)
    except ValidationError as e:
        console.print(f"[bold red]Mapping Schema Error:[/bold red]")
        console.print(e)
        raise typer.Exit(code=1)

def load_prompts(category_filename: str) -> List[VisionPrompt]:
    path = os.path.join("datasets", "vision", "t2i_v0.1", category_filename)
    data = load_yaml(path)
    try:
        pf = PromptFile(**data)
        return pf.prompts
    except ValidationError as e:
        console.print(f"[bold red]Prompt File Schema Error ({category_filename}):[/bold red]")
        console.print(e)
        raise typer.Exit(code=1)

def get_category_filename(category_id: str) -> Optional[str]:
    # Mapping based on implementation
    id_map = {
        "sof": "single_object_fidelity.yaml",
        "moc": "multi_object_composition.yaml",
        "spr": "spatial_relations.yaml",
        "abc": "attribute_binding_counting.yaml",
        "nex": "negation_exclusion.yaml",
        "stb": "style_stability.yaml"
    }
    return id_map.get(category_id)

# --- Commands ---

@app.command("list-categories")
def list_categories():
    """
    List all SemantIQ-Vision benchmark categories.
    """
    registry = load_registry()
    
    console.print(Panel(f"[bold blue]{registry.benchmark_name} v{registry.vision_version}[/bold blue]", expand=False))
    console.print(f"[italic]{registry.evaluation_scope}[/italic]\n")
    
    table = Table(title="Vision Categories")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Rubrics", style="magenta")
    
    for cat in registry.categories:
        table.add_row(
            cat.category_id,
            cat.name,
            ", ".join(cat.primary_rubrics)
        )
    
    console.print(table)
    console.print(f"[dim]Total Categories: {len(registry.categories)}[/dim]")

@app.command("show-category")
def show_category(category_id: str):
    """
    Show details for a specific Vision category, including mapped archetypes.
    """
    registry = load_registry()
    mapping_registry = load_mappings()
    
    cat = next((c for c in registry.categories if c.category_id == category_id), None)
    
    if not cat:
        console.print(f"[bold red]Category '{category_id}' not found.[/bold red]")
        return
    
    console.print(Panel(f"[bold]{cat.name} ({cat.category_id})[/bold]", subtitle="Vision Benchmark Category"))
    
    console.print(f"\n[bold]Description:[/bold]\n{cat.description}")
    
    console.print("\n[bold]Primary Rubrics:[/bold]")
    for r in cat.primary_rubrics:
        console.print(f"- {r}")

    mapping = next((m for m in mapping_registry.mappings.values() if m.category_id == category_id), None)
    
    if mapping:
        console.print("\n[bold]Linked Archetypes:[/bold]")
        if mapping.primary_archetypes:
            console.print(f"  [green]Primary:[/green] {', '.join(mapping.primary_archetypes)}")
        if mapping.secondary_archetypes:
            console.print(f"  [yellow]Secondary:[/yellow] {', '.join(mapping.secondary_archetypes)}")
        if mapping.discouraged_archetypes:
            console.print(f"  [red]Discouraged:[/red] {', '.join(mapping.discouraged_archetypes)}")
        console.print(f"\n[bold]Rationale:[/bold] {mapping.rationale.strip()}")
        
    base_dir = os.path.join("benchmarks", "vision", "categories")
    id_map = {
        "sof": "single_object_fidelity",
        "moc": "multi_object_composition",
        "spr": "spatial_relations",
        "abc": "attribute_binding_counting",
        "nex": "negation_exclusion",
        "stb": "style_stability"
    }
    
    dir_name = id_map.get(category_id)
    if dir_name:
        readme_path = os.path.join(base_dir, dir_name, "README.md")
        if os.path.exists(readme_path):
             console.print(f"\n[bold green]Documentation available at:[/bold green] {readme_path}")

@app.command("list-archetypes")
def list_archetypes():
    """
    List all defined T2I Prompt Archetypes.
    """
    reg = load_archetypes()
    
    table = Table(title=f"Vision Prompt Archetypes v{reg.vision_archetypes_version}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Focus", style="white")
    
    for arch in reg.archetypes:
        table.add_row(
            arch.archetype_id,
            arch.name,
            arch.description.split('.')[0] # First sentence
        )
    
    console.print(table)

@app.command("show-archetype")
def show_archetype(archetype_id: str):
    """
    Show detailed definition of a Prompt Archetype.
    """
    reg = load_archetypes()
    arch = next((a for a in reg.archetypes if a.archetype_id == archetype_id), None)
    
    if not arch:
        console.print(f"[bold red]Archetype '{archetype_id}' not found.[/bold red]")
        return
        
    console.print(Panel(f"[bold]{arch.name} ({arch.archetype_id})[/bold]", subtitle="Prompt Archetype"))
    console.print(f"\n{arch.description}")
    
    console.print("\n[bold]Expected Output Properties:[/bold]")
    for prop in arch.expected_output_properties:
        console.print(f"- {prop}")
        
    console.print("\n[bold]Allowed Variations:[/bold]")
    for var in arch.allowed_variations:
        console.print(f"- {var}")
        
    console.print("\n[bold red]Disallowed Patterns:[/bold red]")
    for pat in arch.disallowed_patterns:
        console.print(f"- {pat}")
        
    console.print("\n[bold yellow]Typical Failure Modes:[/bold yellow]")
    for fail in arch.typical_failure_modes:
        console.print(f"- {fail}")
        
    guideline_path = os.path.join("benchmarks", "vision", "archetypes", archetype_id, "guidelines.md")
    if os.path.exists(guideline_path):
        console.print(f"\n[bold green]Guidelines available at:[/bold green] {guideline_path}")

@app.command("list-prompts")
def list_prompts(category: Optional[str] = None):
    """
    List prompts in the dataset. Optional category filter (use full name like 'spatial_relations').
    """
    # Map friendly names to filenames if needed, or just iterate all
    filenames = [
        "single_object_fidelity.yaml",
        "multi_object_composition.yaml",
        "spatial_relations.yaml",
        "attribute_binding_counting.yaml",
        "negation_exclusion.yaml",
        "style_stability.yaml"
    ]
    
    if category:
        # Simple fuzzy match or exact match on filename stem
        target = category.lower().replace(" ", "_")
        filenames = [f for f in filenames if target in f]
        if not filenames:
            console.print(f"[red]No category found matching '{category}'[/red]")
            return

    table = Table(title="Vision Prompt Set v0.1")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Cat", style="magenta")
    table.add_column("Prompt Text", style="green")
    
    count = 0
    for fname in filenames:
        prompts = load_prompts(fname)
        for p in prompts:
            table.add_row(p.prompt_id, p.category_id, p.prompt_text)
            count += 1
            
    console.print(table)
    console.print(f"[dim]Total Prompts: {count}[/dim]")

@app.command("show-prompt")
def show_prompt(prompt_id: str):
    """
    Show details of a specific prompt by ID.
    """
    filenames = [
        "single_object_fidelity.yaml",
        "multi_object_composition.yaml",
        "spatial_relations.yaml",
        "attribute_binding_counting.yaml",
        "negation_exclusion.yaml",
        "style_stability.yaml"
    ]
    
    found_prompt = None
    for fname in filenames:
        prompts = load_prompts(fname)
        for p in prompts:
            if p.prompt_id == prompt_id:
                found_prompt = p
                break
        if found_prompt:
            break
            
    if not found_prompt:
        console.print(f"[bold red]Prompt '{prompt_id}' not found.[/bold red]")
        return
        
    p = found_prompt
    console.print(Panel(f"[bold]{p.prompt_id}[/bold] ({p.category_id} / {p.archetype_id})", subtitle="Vision Prompt"))
    console.print(f"\n[bold green]\"{p.prompt_text}\"[/bold green]")
    console.print(f"\n[bold]Intent:[/bold] {p.intent}")
    
    console.print("\n[bold]Constraints:[/bold]")
    for c in p.constraints:
        console.print(f"- {c}")
        
    console.print("\n[bold]Expected Properties:[/bold]")
    for ep in p.expected_visual_properties:
        console.print(f"- {ep}")

    console.print("\n[bold yellow]Typical Failure Modes:[/bold yellow]")
    for tfm in p.typical_failure_modes:
        console.print(f"- {tfm}")

@app.command("validate")
def validate():
    """
    Validate all Vision registries, mappings, AND prompt datasets.
    """
    console.print("[bold blue]Validating SemantIQ-Vision Framework...[/bold blue]")
    
    # 1. Load Registry
    reg = load_registry()
    console.print(f"✅ Registry v{reg.vision_version} valid ({len(reg.categories)} categories)")
    
    # 2. Load Archetypes
    arch_reg = load_archetypes()
    console.print(f"✅ Archetypes v{arch_reg.vision_archetypes_version} valid ({len(arch_reg.archetypes)} archetypes)")
    
    # 3. Load Mappings
    map_reg = load_mappings()
    console.print(f"✅ Mappings v{map_reg.category_mapping_version} valid")
    
    # 4. Cross-Reference Validation
    valid_cat_ids = {c.category_id for c in reg.categories}
    valid_arch_ids = {a.archetype_id for a in arch_reg.archetypes}
    
    # Check Mappings against Categories
    for map_key, mapping in map_reg.mappings.items():
        if mapping.category_id not in valid_cat_ids:
            console.print(f"[red]❌ Mapping references unknown category ID: {mapping.category_id}[/red]")
            raise typer.Exit(code=1)
            
        # Check referenced archetypes
        all_referenced = mapping.primary_archetypes + mapping.secondary_archetypes + mapping.discouraged_archetypes
        for arch_id in all_referenced:
            if arch_id not in valid_arch_ids:
                console.print(f"[red]❌ Mapping for {mapping.category_id} references unknown archetype ID: {arch_id}[/red]")
                raise typer.Exit(code=1)

    # Check that every category has at least one primary archetype
    for cat in reg.categories:
        # Find mapping
        found = False
        for m in map_reg.mappings.values():
            if m.category_id == cat.category_id:
                found = True
                if not m.primary_archetypes:
                    console.print(f"[red]❌ Category {cat.category_id} has no primary archetypes defined![/red]")
                    raise typer.Exit(code=1)
                break
        if not found:
            console.print(f"[red]❌ Category {cat.category_id} is missing from mapping file![/red]")
            raise typer.Exit(code=1)

    # 5. Validate Datasets
    console.print("\n[bold]Validating Prompt Datasets...[/bold]")
    filenames = [
        "single_object_fidelity.yaml",
        "multi_object_composition.yaml",
        "spatial_relations.yaml",
        "attribute_binding_counting.yaml",
        "negation_exclusion.yaml",
        "style_stability.yaml"
    ]
    
    total_prompts = 0
    seen_ids = set()
    
    for fname in filenames:
        prompts = load_prompts(fname)
        console.print(f"  - {fname}: {len(prompts)} prompts")
        total_prompts += len(prompts)
        
        for p in prompts:
            # Check ID uniqueness
            if p.prompt_id in seen_ids:
                console.print(f"[red]❌ Duplicate Prompt ID: {p.prompt_id}[/red]")
                raise typer.Exit(code=1)
            seen_ids.add(p.prompt_id)
            
            # Check Category ID validity
            if p.category_id not in valid_cat_ids:
                console.print(f"[red]❌ Prompt {p.prompt_id} references invalid category: {p.category_id}[/red]")
                raise typer.Exit(code=1)
                
            # Check Archetype ID validity
            if p.archetype_id not in valid_arch_ids:
                console.print(f"[red]❌ Prompt {p.prompt_id} references invalid archetype: {p.archetype_id}[/red]")
                raise typer.Exit(code=1)
                
            # Check Constraints
            if not p.constraints:
                console.print(f"[red]❌ Prompt {p.prompt_id} has no constraints![/red]")
                raise typer.Exit(code=1)

    if total_prompts != 30:
        console.print(f"[red]❌ Total prompts must be 30. Found: {total_prompts}[/red]")
        raise typer.Exit(code=1)

    console.print(f"✅ Dataset Integrity Verified ({total_prompts} prompts)")
    console.print("[bold green]All Validation Checks Passed![/bold green]")

@app.command("render")
def render(
    prompt_id: str,
    provider: str = "dummy",
    width: int = 1024,
    height: int = 1024,
    seed: Optional[int] = None
):
    """
    Render a specific prompt by ID.
    """
    # 1. Find Prompt
    filenames = [
        "single_object_fidelity.yaml",
        "multi_object_composition.yaml",
        "spatial_relations.yaml",
        "attribute_binding_counting.yaml",
        "negation_exclusion.yaml",
        "style_stability.yaml"
    ]
    
    found_prompt = None
    for fname in filenames:
        prompts = load_prompts(fname)
        for p in prompts:
            if p.prompt_id == prompt_id:
                found_prompt = p
                break
        if found_prompt:
            break
            
    if not found_prompt:
        console.print(f"[bold red]Prompt '{prompt_id}' not found.[/bold red]")
        raise typer.Exit(code=1)

    # 2. Setup Adapter
    if provider == "dummy":
        adapter = DummyVisionAdapter(model_name="dummy-vision-v1")
    else:
        console.print(f"[yellow]Provider '{provider}' not yet implemented. Using dummy.[/yellow]")
        adapter = DummyVisionAdapter(model_name="dummy-vision-v1")

    # 3. Setup Renderer
    renderer = VisionRenderer(adapter=adapter)
    
    # 4. Render
    params = RenderParams(width=width, height=height, seed=seed)
    
    try:
        result = renderer.render_prompt(found_prompt, params)
        renderer.save_run_metadata(dataset_version="t2i_v0.1") # Save run metadata for single render too
        console.print(f"[green]Successfully rendered {prompt_id}[/green]")
        console.print(f"Image: {result.image_path}")
        console.print(f"Run ID: {renderer.run_id}")
    except Exception as e:
        console.print(f"[red]Rendering failed: {e}[/red]")
        raise typer.Exit(code=1)

@app.command("render-batch")
def render_batch(
    dataset: str = "t2i_v0.1",
    provider: str = "dummy",
    category: Optional[str] = None
):
    """
    Render a batch of prompts (entire dataset or specific category).
    """
    if dataset != "t2i_v0.1":
         console.print(f"[red]Unknown dataset: {dataset}[/red]")
         raise typer.Exit(code=1)

    filenames = [
        "single_object_fidelity.yaml",
        "multi_object_composition.yaml",
        "spatial_relations.yaml",
        "attribute_binding_counting.yaml",
        "negation_exclusion.yaml",
        "style_stability.yaml"
    ]
    
    if category:
        target = category.lower().replace(" ", "_")
        filenames = [f for f in filenames if target in f]
        if not filenames:
             console.print(f"[red]No category found matching '{category}'[/red]")
             raise typer.Exit(code=1)

    # Setup Adapter & Renderer
    if provider == "dummy":
        adapter = DummyVisionAdapter(model_name="dummy-vision-v1")
    else:
        adapter = DummyVisionAdapter(model_name="dummy-vision-v1") # Fallback
        
    renderer = VisionRenderer(adapter=adapter)
    console.print(f"[bold blue]Starting Batch Render (Run ID: {renderer.run_id})[/bold blue]")
    
    params = RenderParams() # Default params
    
    success_count = 0
    total_count = 0
    
    for fname in filenames:
        prompts = load_prompts(fname)
        console.print(f"Processing {fname} ({len(prompts)} prompts)...")
        for p in prompts:
            total_count += 1
            try:
                renderer.render_prompt(p, params)
                success_count += 1
            except Exception as e:
                 console.print(f"[red]Failed {p.prompt_id}: {e}[/red]")

    renderer.save_run_metadata(dataset_version=dataset)
    console.print(f"\n[bold green]Batch Complete: {success_count}/{total_count} rendered.[/bold green]")
    console.print(f"Run Directory: {renderer.base_dir}")

@app.command("show-image")
def show_image(run_id: str, prompt_id: str):
    """
    Show image details and metadata from a run.
    """
    base_dir = os.path.join("runs", "vision", run_id)
    if not os.path.exists(base_dir):
        console.print(f"[red]Run ID '{run_id}' not found.[/red]")
        raise typer.Exit(code=1)
        
    meta_path = os.path.join(base_dir, "metadata", "IMAGE_METADATA.json")
    if not os.path.exists(meta_path):
        console.print(f"[red]Metadata not found for run '{run_id}'.[/red]")
        raise typer.Exit(code=1)
        
    import json
    with open(meta_path, "r") as f:
        data = json.load(f)
        
    # Find entry for prompt_id
    entry = next((item for item in data if item["prompt_id"] == prompt_id), None)
    
    if not entry:
        console.print(f"[red]Prompt '{prompt_id}' not found in run '{run_id}'.[/red]")
        raise typer.Exit(code=1)
        
    console.print(Panel(f"[bold]{prompt_id}[/bold] (Run: {run_id})", subtitle="Image Capture"))
    console.print(f"Provider: {entry['provider']}")
    console.print(f"Model: {entry['model']}")
    console.print(f"Hash: {entry['prompt_hash']}")
    console.print(f"Timestamp: {entry['timestamp']}")
    
    images_dir = os.path.join(base_dir, "images")
    if os.path.exists(images_dir):
        for f in os.listdir(images_dir):
            if f.startswith(f"{prompt_id}_{entry['prompt_hash']}"):
                 console.print(f"\n[bold green]Image File:[/bold green] {os.path.join(images_dir, f)}")
                 break

@app.command("score")
def score(run_id: str):
    """
    Score a completed vision run.
    """
    try:
        engine = VisionScoringEngine()
        report = engine.score_run(run_id)
        
        console.print(Panel(f"[bold]Run Scored: {run_id}[/bold]", subtitle=f"Overall Score: {report.overall_score:.2f}"))
        
        table = Table(title="Category Summaries")
        table.add_column("Category", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Violations", style="red")
        
        for cat_id, summary in report.category_summaries.items():
            table.add_row(
                cat_id,
                f"{summary.mean_score:.2f}",
                f"{summary.violation_rate:.0%}"
            )
        console.print(table)
        
        report_path = os.path.join("reports", "vision", "runs", run_id, "overall_summary.json")
        console.print(f"\n[bold green]Report saved to:[/bold green] {report_path}")
        
    except Exception as e:
        console.print(f"[bold red]Scoring failed:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command("report")
def report(run_id: str):
    """
    Display report for a scored run.
    """
    report_path = os.path.join("reports", "vision", "runs", run_id, "overall_summary.json")
    if not os.path.exists(report_path):
        console.print(f"[red]Report not found for run {run_id}. Run 'bench vision score {run_id}' first.[/red]")
        raise typer.Exit(code=1)
        
    import json
    with open(report_path, "r") as f:
        data = json.load(f)
        
    console.print(Panel(f"[bold]Run Report: {run_id}[/bold]"))
    console.print(f"Provider: {data.get('provider')}")
    console.print(f"Model: {data.get('model')}")
    console.print(f"Overall Score: [bold green]{data.get('overall_score', 0.0):.2f}[/bold green]\n")
    
    summaries = data.get("category_summaries", {})
    for cat_id, summary in summaries.items():
        console.print(f"[bold cyan]{cat_id.upper()}[/bold cyan]: {summary.get('mean_score'):.2f}")
        rubrics = summary.get("rubric_scores", {})
        for r, s in rubrics.items():
             console.print(f"  - {r}: {s:.2f}")
        console.print("")

@app.command("compare")
def compare(run_id_1: str, run_id_2: str):
    """
    Compare two scored runs.
    """
    r1_path = os.path.join("reports", "vision", "runs", run_id_1, "overall_summary.json")
    r2_path = os.path.join("reports", "vision", "runs", run_id_2, "overall_summary.json")
    
    if not os.path.exists(r1_path) or not os.path.exists(r2_path):
        console.print("[red]One or both reports not found. Ensure both runs are scored.[/red]")
        raise typer.Exit(code=1)
        
    import json
    with open(r1_path, "r") as f: d1 = json.load(f)
    with open(r2_path, "r") as f: d2 = json.load(f)
    
    console.print(Panel(f"Comparison: {run_id_1} vs {run_id_2}", subtitle="SemantIQ-Vision"))
    
    table = Table(title="Overall Comparison")
    table.add_column("Metric", style="white")
    table.add_column(f"{d1.get('model')} (R1)", style="cyan")
    table.add_column(f"{d2.get('model')} (R2)", style="magenta")
    table.add_column("Diff", style="yellow")
    
    s1 = d1.get("overall_score", 0.0)
    s2 = d2.get("overall_score", 0.0)
    diff = s2 - s1
    
    table.add_row("Overall Score", f"{s1:.2f}", f"{s2:.2f}", f"{diff:+.2f}")
    console.print(table)
    
    console.print("\n[bold]Category Breakdown:[/bold]")
    cat_table = Table()
    cat_table.add_column("Category", style="white")
    cat_table.add_column("R1 Score", style="cyan")
    cat_table.add_column("R2 Score", style="magenta")
    cat_table.add_column("Diff", style="yellow")
    
    cats = set(d1.get("category_summaries", {}).keys()) | set(d2.get("category_summaries", {}).keys())
    
    for cat in sorted(cats):
        c1 = d1.get("category_summaries", {}).get(cat, {}).get("mean_score", 0.0)
        c2 = d2.get("category_summaries", {}).get(cat, {}).get("mean_score", 0.0)
        cdiff = c2 - c1
        cat_table.add_row(cat, f"{c1:.2f}", f"{c2:.2f}", f"{cdiff:+.2f}")
        
    console.print(cat_table)

if __name__ == "__main__":
    app()
