import typer
import yaml
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError

app = typer.Typer(name="smf", help="Semantic Maturity Framework (SMF) commands")
console = Console()

# --- Schema Definition for Validation ---
class Subdimension(str):
    pass

class Category(BaseModel):
    category_id: str
    name: str
    description: str
    measured_capability: str
    maturity_focus: str
    benchmark_type: str
    extension: bool
    subdimensions: List[str]

class SMFRegistry(BaseModel):
    smf_version: str
    framework_name: str
    categories: List[Category]

class BenchmarkType(BaseModel):
    type_id: str
    name: str
    description: str
    typical_output_format: str
    evaluation_style: str
    risk_profile: List[str]
    allowed_prompt_structure: List[str]

class CategoryMapping(BaseModel):
    allowed_types: List[str]
    discouraged_types: List[str]
    rationale: str

class QuestionArchetype(BaseModel):
    archetype_id: str
    category_id: str
    benchmark_type: str
    name: str
    intent: str
    input_structure: str
    expected_output_characteristics: str
    variation_axes: List[str]
    disallowed_patterns: List[str]
    typical_failure_modes: List[str]
    scoring_hints: str

class ArchetypeRegistry(BaseModel):
    archetypes: List[QuestionArchetype]

# --- Helper Functions ---
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

def load_registry(registry_path: str = "benchmarks/smf/registry.yaml") -> Dict[str, Any]:
    return load_yaml(registry_path)

def load_benchmark_types(path: str = "benchmarks/smf/benchmark_types.yaml") -> List[Dict[str, Any]]:
    return load_yaml(path)

def load_mapping(path: str = "benchmarks/smf/category_task_mapping.yaml") -> Dict[str, Any]:
    return load_yaml(path)

def load_archetypes(path: str = "benchmarks/smf/question_archetypes.yaml") -> Dict[str, Any]:
    return load_yaml(path)

def validate_registry_schema(data: Dict[str, Any]) -> SMFRegistry:
    try:
        return SMFRegistry(**data)
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] Registry schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

def validate_archetypes_schema(data: Dict[str, Any]) -> ArchetypeRegistry:
    try:
        return ArchetypeRegistry(**data)
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] Archetypes schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

def validate_types_schema(data: List[Dict[str, Any]]) -> List[BenchmarkType]:
    try:
        return [BenchmarkType(**item) for item in data]
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] Benchmark types schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

def validate_logic(registry: SMFRegistry):
    """Additional logical validation"""
    ids = [c.category_id for c in registry.categories]
    if len(ids) != len(set(ids)):
        console.print("[bold red]Validation Error:[/bold red] Duplicate category_ids found.")
        raise typer.Exit(code=1)
    
    for cat in registry.categories:
        if not cat.subdimensions:
            console.print(f"[bold red]Validation Error:[/bold red] Category {cat.category_id} has no subdimensions.")
            raise typer.Exit(code=1)

def validate_archetype_logic(archetypes: ArchetypeRegistry, registry: SMFRegistry, types: List[BenchmarkType]):
    cat_ids = {c.category_id for c in registry.categories}
    type_ids = {t.type_id for t in types}
    arch_ids = set()

    for arch in archetypes.archetypes:
        if arch.category_id not in cat_ids:
             console.print(f"[bold red]Validation Error:[/bold red] Archetype {arch.archetype_id} references unknown category {arch.category_id}")
             raise typer.Exit(code=1)
        if arch.benchmark_type not in type_ids:
             console.print(f"[bold red]Validation Error:[/bold red] Archetype {arch.archetype_id} references unknown benchmark type {arch.benchmark_type}")
             raise typer.Exit(code=1)
        if arch.archetype_id in arch_ids:
             console.print(f"[bold red]Validation Error:[/bold red] Duplicate archetype_id {arch.archetype_id}")
             raise typer.Exit(code=1)
        arch_ids.add(arch.archetype_id)

# --- Commands ---

@app.command("list-categories")
def list_categories():
    """
    List all SMF categories defined in the registry.
    """
    data = load_registry()
    registry = validate_registry_schema(data)
    validate_logic(registry)
    
    console.print(Panel(f"[bold blue]{registry.framework_name} v{registry.smf_version}[/bold blue]", expand=False))
    
    table = Table(title="SMF Categories")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Focus", style="magenta")
    table.add_column("Type", style="yellow")
    table.add_column("Ext.", style="dim")
    table.add_column("Capability", style="white")
    
    for cat in registry.categories:
        table.add_row(
            cat.category_id,
            cat.name,
            cat.maturity_focus,
            cat.benchmark_type,
            "Yes" if cat.extension else "No",
            cat.measured_capability
        )
    
    console.print(table)
    console.print(f"[dim]Total Categories: {len(registry.categories)}[/dim]")

@app.command("list-benchmark-types")
def list_benchmark_types():
    """
    List all official SMF benchmark types.
    """
    data = load_benchmark_types()
    types = validate_types_schema(data)
    
    table = Table(title="SMF Benchmark Types")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Format", style="magenta")
    table.add_column("Eval Style", style="yellow")
    
    for t in types:
        table.add_row(t.type_id, t.name, t.typical_output_format, t.evaluation_style)
        
    console.print(table)

@app.command("show-category")
def show_category(category_id: str):
    """
    Show detailed information for a specific category, including allowed task types.
    """
    # Load Registry
    reg_data = load_registry()
    registry = validate_registry_schema(reg_data)
    
    # Load Mapping
    map_data = load_mapping()
    
    category = next((c for c in registry.categories if c.category_id == category_id), None)
    if not category:
        console.print(f"[bold red]Category '{category_id}' not found.[/bold red]")
        return
    
    console.print(Panel(f"[bold]{category.name} ({category.category_id})[/bold]", subtitle=category.maturity_focus))
    console.print(f"[italic]{category.description}[/italic]\n")
    console.print(f"[bold]Measured Capability:[/bold] {category.measured_capability}")
    console.print(f"[bold]Benchmark Type:[/bold] {category.benchmark_type}")
    
    console.print("\n[bold]Subdimensions:[/bold]")
    for sub in category.subdimensions:
        console.print(f"- {sub}")
        
    # Show Mapping Info
    if category_id in map_data:
        mapping = CategoryMapping(**map_data[category_id])
        console.print("\n[bold]Benchmark Type Mapping:[/bold]")
        console.print(f"[green]Allowed:[/green] {', '.join(mapping.allowed_types)}")
        console.print(f"[red]Discouraged:[/red] {', '.join(mapping.discouraged_types)}")
        console.print(f"[dim]Rationale: {mapping.rationale}[/dim]")
    else:
        console.print("\n[bold red]No task mapping found for this category![/bold red]")
    
    # Try to load README
    readme_path = os.path.join("benchmarks", "smf", "categories", category_id, "README.md")
    if not os.path.exists(readme_path):
         readme_path = os.path.join("benchmarks", "smf", "extensions", category_id, "README.md")
         
    if os.path.exists(readme_path):
        console.print(f"\n[bold green]Documentation available at:[/bold green] {readme_path}")

@app.command("list-archetypes")
def list_archetypes(category: str = typer.Option(None, help="Filter by category ID")):
    """
    List all question archetypes, optionally filtered by category.
    """
    data = load_archetypes()
    registry = validate_archetypes_schema(data)
    
    table = Table(title=f"SMF Question Archetypes{' (' + category + ')' if category else ''}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Category", style="blue")
    table.add_column("Type", style="yellow")
    table.add_column("Name", style="green")
    table.add_column("Intent", style="white")
    
    for arch in registry.archetypes:
        if category and arch.category_id != category:
            continue
        table.add_row(arch.archetype_id, arch.category_id, arch.benchmark_type, arch.name, arch.intent)
        
    console.print(table)

@app.command("show-archetype")
def show_archetype(archetype_id: str):
    """
    Show detailed definition of a specific archetype.
    """
    data = load_archetypes()
    registry = validate_archetypes_schema(data)
    
    arch = next((a for a in registry.archetypes if a.archetype_id == archetype_id), None)
    
    if not arch:
        console.print(f"[bold red]Archetype '{archetype_id}' not found.[/bold red]")
        return
        
    console.print(Panel(f"[bold]{arch.name} ({arch.archetype_id})[/bold]", subtitle=f"Category: {arch.category_id} | Type: {arch.benchmark_type}"))
    
    console.print(f"\n[bold]Intent:[/bold] {arch.intent}")
    console.print(f"[bold]Input Structure:[/bold] {arch.input_structure}")
    console.print(f"[bold]Expected Output:[/bold] {arch.expected_output_characteristics}")
    
    console.print("\n[bold]Variation Axes:[/bold]")
    for axis in arch.variation_axes:
        console.print(f"- {axis}")

    console.print("\n[bold red]Disallowed Patterns:[/bold red]")
    for p in arch.disallowed_patterns:
        console.print(f"- {p}")
        
    console.print("\n[bold yellow]Typical Failure Modes:[/bold yellow]")
    for m in arch.typical_failure_modes:
        console.print(f"- {m}")
        
    console.print(f"\n[dim]Scoring Hints: {arch.scoring_hints}[/dim]")

@app.command("validate")
def validate():
    """
    Validate the SMF registry integrity.
    """
    # Validate Registry
    reg_data = load_registry()
    registry = validate_registry_schema(reg_data)
    validate_logic(registry)
    
    # Validate Types
    type_data = load_benchmark_types()
    types = validate_types_schema(type_data)
    
    # Validate Archetypes
    arch_data = load_archetypes()
    archetypes = validate_archetypes_schema(arch_data)
    validate_archetype_logic(archetypes, registry, types)
    
    console.print("[bold green]SMF Registry and Archetypes are valid![/bold green]")

if __name__ == "__main__":
    app()
