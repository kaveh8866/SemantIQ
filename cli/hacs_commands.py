import typer
import yaml
import json
import os
import hashlib
import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ValidationError

# Import Scoring Engine
from benchmarks.hacs.scoring import HACSScoringEngine, ScoreResult, OverallReport

app = typer.Typer(name="hacs", help="Human-AI Comparative Score (HACS) commands")
console = Console()

# --- Schema Definition for Validation ---
class HACSModule(BaseModel):
    module_id: str
    name: str
    directory: str
    question_count: int
    measured_capabilities: List[str]
    related_smf_categories: List[str]

class HACSArchetype(BaseModel):
    archetype_id: str
    module_id: str
    name: str
    intent: str
    elicited_criteria: List[str]
    input_pattern: str
    response_expectation: str
    allowed_variations: List[str]
    disallowed_patterns: List[str]
    typical_failure_modes: Dict[str, str]

class HACSQuestion(BaseModel):
    question_id: str
    module_id: str
    archetype_id: str
    question_text: str
    elicited_criteria: List[str]
    constraints: str
    expected_response_characteristics: str
    difficulty: str
    language: str
    version: str

class HACSScoringCriteria(BaseModel):
    name: str
    description: str

class HACSScoringModel(BaseModel):
    criteria: List[HACSScoringCriteria]
    maturity_levels: Dict[str, List[float]]

class HACSRegistry(BaseModel):
    hacs_version: str
    framework_name: str
    purpose: str
    symmetry_principle: str
    total_questions: int
    scoring_model_reference: HACSScoringModel
    modules: List[HACSModule]

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

def load_hacs_registry(path: str = "benchmarks/hacs/registry.yaml") -> Dict[str, Any]:
    return load_yaml(path)

def load_hacs_archetypes(path: str = "benchmarks/hacs/question_archetypes.yaml") -> List[Dict[str, Any]]:
    return load_yaml(path)

def load_hacs_questions(base_path: str = "datasets/hacs/hib_1.0") -> List[Dict[str, Any]]:
    questions = []
    files = [
        "h1_meaning_context.yaml",
        "h2_bias_resilience.yaml",
        "h3_knowledge_illusion.yaml",
        "h4_reflection_metacognition.yaml",
        "h5_longform_consistency.yaml"
    ]
    for filename in files:
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            qs = load_yaml(path)
            if qs:
                questions.extend(qs)
    return questions

def validate_hacs_schema(data: Dict[str, Any]) -> HACSRegistry:
    try:
        registry = HACSRegistry(**data)
        
        # Logical Validation
        total_q = sum(m.question_count for m in registry.modules)
        if total_q != 70:
            console.print(f"[bold red]Validation Error:[/bold red] Total questions must be 70 (found {total_q}).")
            raise typer.Exit(code=1)
            
        for m in registry.modules:
            if m.question_count < 10:
                console.print(f"[bold red]Validation Error:[/bold red] Module {m.module_id} has fewer than 10 questions ({m.question_count}).")
                raise typer.Exit(code=1)
        
        return registry
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] HACS Registry schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

def validate_hacs_archetypes_schema(data: List[Dict[str, Any]], registry: HACSRegistry) -> List[HACSArchetype]:
    archetypes = []
    seen_ids = set()
    valid_module_ids = {m.module_id for m in registry.modules}
    valid_criteria = {c.name.lower() for c in registry.scoring_model_reference.criteria}

    try:
        for item in data:
            arch = HACSArchetype(**item)
            
            # 1. Unique ID check
            if arch.archetype_id in seen_ids:
                console.print(f"[bold red]Validation Error:[/bold red] Duplicate archetype ID found: {arch.archetype_id}")
                raise typer.Exit(code=1)
            seen_ids.add(arch.archetype_id)

            # 2. Module existence check
            if arch.module_id not in valid_module_ids:
                console.print(f"[bold red]Validation Error:[/bold red] Archetype {arch.archetype_id} refers to unknown module: {arch.module_id}")
                raise typer.Exit(code=1)

            # 3. Criteria subset check
            for criterion in arch.elicited_criteria:
                if criterion.lower() not in valid_criteria:
                    console.print(f"[bold red]Validation Error:[/bold red] Archetype {arch.archetype_id} has invalid criterion: {criterion}")
                    raise typer.Exit(code=1)
            
            archetypes.append(arch)
            
        return archetypes
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] HACS Archetype schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

def validate_hacs_questions_schema(data: List[Dict[str, Any]], registry: HACSRegistry, archetypes: List[HACSArchetype]) -> List[HACSQuestion]:
    questions = []
    seen_ids = set()
    valid_module_ids = {m.module_id for m in registry.modules}
    valid_archetype_ids = {a.archetype_id for a in archetypes}
    valid_criteria = {c.name.lower() for c in registry.scoring_model_reference.criteria}

    try:
        for item in data:
            q = HACSQuestion(**item)

            # 1. Unique ID check
            if q.question_id in seen_ids:
                console.print(f"[bold red]Validation Error:[/bold red] Duplicate question ID found: {q.question_id}")
                raise typer.Exit(code=1)
            seen_ids.add(q.question_id)

            # 2. Module existence check
            if q.module_id not in valid_module_ids:
                console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} refers to unknown module: {q.module_id}")
                raise typer.Exit(code=1)

            # 3. Archetype existence check
            if q.archetype_id not in valid_archetype_ids:
                console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} refers to unknown archetype: {q.archetype_id}")
                raise typer.Exit(code=1)

            # 4. Criteria check (>=2, valid subset)
            if len(q.elicited_criteria) < 2:
                console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} must elicit at least 2 criteria.")
                raise typer.Exit(code=1)
            
            for criterion in q.elicited_criteria:
                if criterion.lower() not in valid_criteria:
                    console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} has invalid criterion: {criterion}")
                    raise typer.Exit(code=1)

            # 5. Difficulty check
            if q.difficulty not in ["low", "medium", "high"]:
                console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} has invalid difficulty: {q.difficulty}")
                raise typer.Exit(code=1)

            # 6. Language check
            if q.language not in ["en", "de"]:
                console.print(f"[bold red]Validation Error:[/bold red] Question {q.question_id} has invalid language: {q.language}")
                raise typer.Exit(code=1)

            questions.append(q)

        return questions
    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] HACS Question schema is invalid.")
        console.print(e)
        raise typer.Exit(code=1)

# --- Commands ---

@app.command("list-modules")
def list_modules():
    """
    List all HACS modules defined in the registry.
    """
    data = load_hacs_registry()
    registry = validate_hacs_schema(data)
    
    console.print(Panel(f"[bold blue]{registry.framework_name} ({registry.hacs_version})[/bold blue]", expand=False))
    console.print(f"[italic]{registry.purpose}[/italic]\n")
    
    table = Table(title="HACS Modules")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Q Count", style="magenta")
    table.add_column("SMF Relation", style="yellow")
    
    for mod in registry.modules:
        table.add_row(
            mod.module_id,
            mod.name,
            str(mod.question_count),
            ", ".join(mod.related_smf_categories)
        )
    
    console.print(table)
    console.print(f"[dim]Total Questions: {registry.total_questions}[/dim]")

@app.command("show-module")
def show_module(module_id: str):
    """
    Show detailed information for a specific HACS module.
    """
    data = load_hacs_registry()
    registry = validate_hacs_schema(data)
    
    module = next((m for m in registry.modules if m.module_id == module_id), None)
    
    if not module:
        console.print(f"[bold red]Module '{module_id}' not found.[/bold red]")
        return
    
    console.print(Panel(f"[bold]{module.name} ({module.module_id})[/bold]", subtitle=f"Questions: {module.question_count}"))
    
    console.print("\n[bold]Measured Capabilities:[/bold]")
    for cap in module.measured_capabilities:
        console.print(f"- {cap}")
        
    console.print(f"\n[bold]Related SMF Categories:[/bold] {', '.join(module.related_smf_categories)}")
    
    readme_path = os.path.join("benchmarks", "hacs", "modules", module.directory, "README.md")
    if os.path.exists(readme_path):
        console.print(f"\n[bold green]Documentation available at:[/bold green] {readme_path}")
    else:
        console.print(f"\n[yellow]README not found at {readme_path}[/yellow]")

@app.command("list-archetypes")
def list_archetypes(module: Optional[str] = typer.Option(None, "--module", "-m", help="Filter by module ID")):
    """
    List HACS question archetypes, optionally filtered by module.
    """
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    
    if module:
        archetypes = [a for a in archetypes if a.module_id == module]
        if not archetypes:
            console.print(f"[yellow]No archetypes found for module '{module}'.[/yellow]")
            return

    table = Table(title=f"HACS Question Archetypes{' (Module: ' + module + ')' if module else ''}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Module", style="green")
    table.add_column("Name", style="magenta")
    table.add_column("Criteria", style="yellow")
    
    for arch in archetypes:
        table.add_row(
            arch.archetype_id,
            arch.module_id,
            arch.name,
            ", ".join(arch.elicited_criteria)
        )
    
    console.print(table)
    console.print(f"[dim]Total Archetypes: {len(archetypes)}[/dim]")

@app.command("list-questions")
def list_questions(module: Optional[str] = typer.Option(None, "--module", "-m", help="Filter by module ID")):
    """
    List HACS questions, optionally filtered by module.
    """
    # Load context
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    
    questions_data = load_hacs_questions()
    questions = validate_hacs_questions_schema(questions_data, registry, archetypes)

    if module:
        questions = [q for q in questions if q.module_id == module]
        if not questions:
            console.print(f"[yellow]No questions found for module '{module}'.[/yellow]")
            return

    table = Table(title=f"HACS Questions{' (Module: ' + module + ')' if module else ''}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Module", style="green")
    table.add_column("Archetype", style="magenta")
    table.add_column("Difficulty", style="yellow")
    table.add_column("Preview", style="white")

    for q in questions:
        preview = q.question_text[:50] + "..." if len(q.question_text) > 50 else q.question_text
        table.add_row(
            q.question_id,
            q.module_id,
            q.archetype_id,
            q.difficulty,
            preview
        )
    
    console.print(table)
    console.print(f"[dim]Total Questions: {len(questions)}[/dim]")

@app.command("show-question")
def show_question(question_id: str):
    """
    Show detailed information for a specific HACS question.
    """
    # Load context
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    
    questions_data = load_hacs_questions()
    questions = validate_hacs_questions_schema(questions_data, registry, archetypes)

    question = next((q for q in questions if q.question_id == question_id), None)
    
    if not question:
        console.print(f"[bold red]Question '{question_id}' not found.[/bold red]")
        return
    
    console.print(Panel(f"[bold]Question: {question.question_id}[/bold]", subtitle=f"Module: {question.module_id} | Archetype: {question.archetype_id}"))
    
    console.print(Panel(question.question_text, title="Task Prompt", style="bold white"))
    
    console.print(f"\n[bold]Elicited Criteria:[/bold] {', '.join(question.elicited_criteria)}")
    console.print(f"[bold]Difficulty:[/bold] {question.difficulty}")
    console.print(f"[bold]Language:[/bold] {question.language}")
    
    console.print(f"\n[bold]Constraints:[/bold] {question.constraints}")
    console.print(f"\n[bold]Expected Response Characteristics:[/bold]")
    console.print(f"[italic]{question.expected_response_characteristics}[/italic]")

@app.command("show-archetype")
def show_archetype(archetype_id: str):
    """
    Show detailed information for a specific HACS archetype.
    """
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    
    arch = next((a for a in archetypes if a.archetype_id == archetype_id), None)
    
    if not arch:
        console.print(f"[bold red]Archetype '{archetype_id}' not found.[/bold red]")
        return
    
    console.print(Panel(f"[bold]{arch.name} ({arch.archetype_id})[/bold]", subtitle=f"Module: {arch.module_id}"))
    
    console.print(f"\n[bold]Intent:[/bold] {arch.intent}")
    console.print(f"[bold]Elicited Criteria:[/bold] {', '.join(arch.elicited_criteria)}")
    
    console.print(f"\n[bold]Input Pattern:[/bold]")
    console.print(Panel(arch.input_pattern, style="italic"))
    
    console.print(f"[bold]Response Expectation:[/bold] {arch.response_expectation}")
    
    console.print("\n[bold]Allowed Variations:[/bold]")
    for var in arch.allowed_variations:
        console.print(f"- {var}")
        
    console.print("\n[bold]Disallowed Patterns:[/bold]")
    for pat in arch.disallowed_patterns:
        console.print(f"- {pat}")

    console.print("\n[bold]Typical Failure Modes:[/bold]")
    for actor, mode in arch.typical_failure_modes.items():
        console.print(f"- [bold]{actor}:[/bold] {mode}")

@app.command("validate")
def validate():
    """
    Validate the HACS registry and archetype integrity.
    """
    # Registry Validation
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    console.print("[bold green]HACS Registry is valid![/bold green]")
    
    # Archetype Validation
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    console.print(f"[bold green]HACS Archetypes are valid! ({len(archetypes)} archetypes loaded)[/bold green]")
    
    # Verify Minimum Archetypes per Module
    # H1=4, H2=5, H3=4, H4=3, H5=3
    min_requirements = {"h1": 4, "h2": 5, "h3": 4, "h4": 3, "h5": 3}
    for mod_id, min_count in min_requirements.items():
        count = sum(1 for a in archetypes if a.module_id == mod_id)
        if count < min_count:
             console.print(f"[bold red]Validation Error:[/bold red] Module {mod_id} has {count} archetypes, requires {min_count}.")
             raise typer.Exit(code=1)
    
    console.print("[bold green]All module minimum requirements met![/bold green]")

    # Question Validation
    questions_data = load_hacs_questions()
    questions = validate_hacs_questions_schema(questions_data, registry, archetypes)
    console.print(f"[bold green]HACS Questions are valid! ({len(questions)} questions loaded)[/bold green]")

    # Verify Question Count (70)
    if len(questions) != 70:
        console.print(f"[bold red]Validation Error:[/bold red] Total questions must be 70 (found {len(questions)}).")
        raise typer.Exit(code=1)
    
    # Verify Questions per Module (Matches Registry)
    for mod in registry.modules:
        count = sum(1 for q in questions if q.module_id == mod.module_id)
        if count != mod.question_count:
            console.print(f"[bold red]Validation Error:[/bold red] Module {mod.module_id} has {count} questions, requires {mod.question_count}.")
            raise typer.Exit(code=1)
            
    console.print("[bold green]All question count requirements met![/bold green]")


@app.command("render")
def render(question_id: str):
    """
    Render a HACS question prompt and generate its deterministic hash.
    """
    # 1. Load Question
    registry_data = load_hacs_registry()
    registry = validate_hacs_schema(registry_data)
    archetypes_data = load_hacs_archetypes()
    archetypes = validate_hacs_archetypes_schema(archetypes_data, registry)
    questions_data = load_hacs_questions()
    questions = validate_hacs_questions_schema(questions_data, registry, archetypes)

    question = next((q for q in questions if q.question_id == question_id), None)
    if not question:
        console.print(f"[bold red]Question '{question_id}' not found.[/bold red]")
        raise typer.Exit(code=1)

    # 2. Load Templates
    template_dir = os.path.join("prompts", "hacs", "core", "v1")
    manifest_path = os.path.join(template_dir, "manifest.yaml")
    system_path = os.path.join(template_dir, "system.md")
    user_path = os.path.join(template_dir, "user.md")

    if not all(os.path.exists(p) for p in [manifest_path, system_path, user_path]):
        console.print(f"[bold red]Template files missing in {template_dir}[/bold red]")
        raise typer.Exit(code=1)

    manifest = load_yaml(manifest_path)
    with open(system_path, "r", encoding="utf-8") as f:
        system_template = f.read()
    with open(user_path, "r", encoding="utf-8") as f:
        user_template = f.read()

    # 3. Render User Prompt
    # Strict substitution
    rendered_user = user_template.replace("{{question_text}}", question.question_text)
    rendered_user = rendered_user.replace("{{constraints}}", question.constraints)

    # 4. Generate Hash
    # Hash = SHA256(template_id + version + question_id + rendered_system + rendered_user)
    # Note: System prompt is constant but included for completeness of the "prompt state"
    hash_input = f"{manifest['template_id']}{manifest['version']}{question.question_id}{system_template}{rendered_user}"
    prompt_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    # 5. Output
    console.print(Panel(f"[bold blue]HACS Prompt Render[/bold blue] (Hash: {prompt_hash[:12]})", expand=False))
    
    console.print(f"\n[bold]System Prompt ({len(system_template)} chars):[/bold]")
    console.print(Panel(system_template, style="dim"))

    console.print(f"\n[bold]User Prompt ({len(rendered_user)} chars):[/bold]")
    console.print(Panel(rendered_user, style="white"))
    
    console.print(f"\n[bold]Full Hash:[/bold] {prompt_hash}")
    console.print(f"[bold]Template ID:[/bold] {manifest['template_id']} (v{manifest['version']})")


@app.command("show-template")
def show_template():
    """
    Show the raw HACS system and user templates.
    """
    template_dir = os.path.join("prompts", "hacs", "core", "v1")
    system_path = os.path.join(template_dir, "system.md")
    user_path = os.path.join(template_dir, "user.md")
    manifest_path = os.path.join(template_dir, "manifest.yaml")

    if not all(os.path.exists(p) for p in [manifest_path, system_path, user_path]):
        console.print(f"[bold red]Template files missing in {template_dir}[/bold red]")
        raise typer.Exit(code=1)
    
    manifest = load_yaml(manifest_path)
    
    console.print(Panel(f"[bold]HACS Core Template (v{manifest['version']})[/bold]", subtitle=manifest['template_id']))
    
    with open(system_path, "r", encoding="utf-8") as f:
        console.print("\n[bold]System Template (system.md):[/bold]")
        console.print(Panel(f.read(), style="dim"))

    with open(user_path, "r", encoding="utf-8") as f:
        console.print("\n[bold]User Template (user.md):[/bold]")
        console.print(Panel(f.read(), style="white"))
        
    console.print("\n[bold]Manifest:[/bold]")
    console.print(manifest)


@app.command("score")
def score(run_id: str = typer.Argument(..., help="ID of the run to score")):
    """
    Score a HACS run using the 6-criteria rubric.
    Expected input: runs/<run_id>/result.json
    """
    # 1. Load Data
    run_dir = os.path.join("runs", run_id)
    input_path = os.path.join(run_dir, "result.json")
    
    if not os.path.exists(input_path):
        console.print(f"[bold red]Run results not found at {input_path}[/bold red]")
        raise typer.Exit(code=1)
        
    with open(input_path, "r", encoding="utf-8") as f:
        run_data = json.load(f)
        
    # run_data might be a list or a dict with "results" key
    results_list = run_data if isinstance(run_data, list) else run_data.get("results", [])
    
    # 2. Load Questions for Context
    # We need full context for scoring
    console.print("Loading registry and questions...")
    registry = validate_hacs_schema(load_hacs_registry())
    archetypes = validate_hacs_archetypes_schema(load_hacs_archetypes(), registry)
    questions = validate_hacs_questions_schema(load_hacs_questions(), registry, archetypes)
    
    q_map = {q.question_id: q.dict() for q in questions}
    
    # 3. Initialize Engine
    engine = HACSScoringEngine()
    scored_results = []
    
    with console.status("[bold green]Scoring responses...[/bold green]"):
        for item in results_list:
            qid = item.get("question_id")
            response = item.get("response") or item.get("output")
            
            if not qid or not response:
                continue
                
            q_data = q_map.get(qid)
            if not q_data:
                console.print(f"[yellow]Warning: Question {qid} not found in registry. Skipping.[/yellow]")
                continue
                
            score_res = engine.score_question(qid, response, q_data)
            scored_results.append(score_res)
            
    # 4. Aggregate & Report
    # Create output directory
    report_dir = os.path.join("reports", "hacs", "runs", run_id)
    os.makedirs(report_dir, exist_ok=True)
    
    report = engine.generate_report(run_id, scored_results, {}) 
    
    # Save artifacts
    with open(os.path.join(report_dir, "individual_scores.json"), "w", encoding="utf-8") as f:
        json.dump([r.dict() for r in scored_results], f, indent=2)
        
    with open(os.path.join(report_dir, "overall_summary.json"), "w", encoding="utf-8") as f:
        json.dump(report.dict(), f, indent=2)
        
    console.print(Panel(f"[bold green]Scoring Complete for {run_id}[/bold green]", expand=False))
    console.print(f"Overall Score: [bold]{report.overall_score}[/bold] ({report.maturity_level})")
    console.print(f"Reports saved to: {report_dir}")

@app.command("report")
def report(run_id: str):
    """
    Display the HACS summary report for a scored run.
    """
    report_path = os.path.join("reports", "hacs", "runs", run_id, "overall_summary.json")
    if not os.path.exists(report_path):
        console.print(f"[bold red]Report not found at {report_path}. Run 'bench hacs score {run_id}' first.[/bold red]")
        raise typer.Exit(code=1)
        
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        report = OverallReport(**data)
        
    console.print(Panel(f"[bold blue]HACS Report: {run_id}[/bold blue]", subtitle=f"Maturity: {report.maturity_level.upper()}"))
    console.print(f"Overall Score: [bold cyan]{report.overall_score}[/bold cyan]")
    
    table = Table(title="Module Performance")
    table.add_column("Module", style="cyan")
    table.add_column("Score", style="magenta")
    table.add_column("Variance", style="yellow")
    table.add_column("Questions", style="white")
    
    for mod_id, summary in report.module_summaries.items():
        table.add_row(
            mod_id,
            str(summary.overall_module_score),
            str(summary.variance),
            str(summary.question_count)
        )
    console.print(table)

@app.command("compare")
def compare(run1_id: str, run2_id: str):
    """
    Compare two HACS runs side-by-side.
    """
    path1 = os.path.join("reports", "hacs", "runs", run1_id, "overall_summary.json")
    path2 = os.path.join("reports", "hacs", "runs", run2_id, "overall_summary.json")
    
    if not os.path.exists(path1) or not os.path.exists(path2):
        console.print("[bold red]One or both reports missing. Ensure both runs are scored.[/bold red]")
        raise typer.Exit(code=1)
        
    with open(path1, "r") as f: r1 = OverallReport(**json.load(f))
    with open(path2, "r") as f: r2 = OverallReport(**json.load(f))
    
    console.print(Panel(f"[bold]HACS Comparison: {run1_id} vs {run2_id}[/bold]", expand=False))
    
    table = Table(title="Overall Comparison")
    table.add_column("Metric", style="white")
    table.add_column(f"{run1_id}", style="cyan")
    table.add_column(f"{run2_id}", style="magenta")
    table.add_column("Diff", style="yellow")
    
    diff = r2.overall_score - r1.overall_score
    table.add_row(
        "Overall Score",
        str(r1.overall_score),
        str(r2.overall_score),
        f"{diff:+.2f}"
    )
    table.add_row(
        "Maturity",
        r1.maturity_level,
        r2.maturity_level,
        "-"
    )
    console.print(table)
    
    # Module diffs
    mod_table = Table(title="Module Differences")
    mod_table.add_column("Module", style="white")
    mod_table.add_column(f"{run1_id}", style="cyan")
    mod_table.add_column(f"{run2_id}", style="magenta")
    
    all_mods = set(r1.module_summaries.keys()) | set(r2.module_summaries.keys())
    for mod in sorted(all_mods):
        s1 = r1.module_summaries.get(mod).overall_module_score if mod in r1.module_summaries else 0.0
        s2 = r2.module_summaries.get(mod).overall_module_score if mod in r2.module_summaries else 0.0
        mod_table.add_row(mod, str(s1), str(s2))
        
    console.print(mod_table)


@app.command("validate-scoring")
def validate_scoring():
    """
    Run the HACS scoring validation suite (Unit Tests + Golden Set Calibration).
    """
    console.print("[bold blue]Running HACS Scoring Validation Suite...[/bold blue]\n")

    # 1. Run Unit Tests
    console.print("[bold]1. Executing Unit Tests (tests/hacs/test_scoring.py)[/bold]")
    test_result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests/hacs/test_scoring.py"],
        capture_output=True,
        text=True
    )
    
    if test_result.returncode == 0:
        console.print("[bold green]✔ Unit Tests Passed[/bold green]")
        # console.print(test_result.stderr) # Unittest prints to stderr
    else:
        console.print("[bold red]✘ Unit Tests Failed[/bold red]")
        console.print(test_result.stderr)
        raise typer.Exit(code=1)

    console.print("\n[bold]2. Executing Golden Set Calibration (benchmarks/hacs/calibration.py)[/bold]")
    # 2. Run Calibration
    calib_result = subprocess.run(
        [sys.executable, "benchmarks/hacs/calibration.py"],
        capture_output=True,
        text=True
    )

    print(calib_result.stdout) # Print calibration output directly

    if calib_result.returncode == 0:
        console.print("[bold green]✔ Calibration Passed[/bold green]")
    else:
        console.print("[bold red]✘ Calibration Failed[/bold red]")
        raise typer.Exit(code=1)

    console.print("\n[bold green]All Validation Checks Passed Successfully![/bold green]")


if __name__ == "__main__":
    app()
