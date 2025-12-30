import typer
import json
import pandas as pd
import os
from rich.console import Console
from rich.table import Table
from evaluation.reliability import calculate_icc, calculate_krippendorff_alpha
from evaluation.reliability.utils import load_ratings, create_reliability_matrix, generate_data_manifest

app = typer.Typer(help="Research and Validation Commands")
console = Console()

@app.command()
def validate_hacs(
    ratings: str = typer.Option(..., "--ratings", "-r", help="Path to the HACS ratings CSV file"),
    schema: str = typer.Option("datasets/hacs/ratings/schema.json", "--schema", "-s", help="Path to schema.json")
):
    """
    Validate a HACS ratings CSV file against the official schema.
    """
    try:
        df = pd.read_csv(ratings)
        console.print(f"[green]Loaded {len(df)} ratings from {ratings}[/green]")
    except Exception as e:
        console.print(f"[red]Error loading CSV:[/red] {e}")
        raise typer.Exit(code=1)

    try:
        with open(schema, 'r') as f:
            schema_data = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading schema:[/red] {e}")
        raise typer.Exit(code=1)

    # Basic Schema Validation
    required_cols = schema_data.get("required", [])
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        console.print(f"[red]Validation Failed![/red] Missing columns: {missing_cols}")
        raise typer.Exit(code=1)
        
    # Data Type Validation (Simple Check)
    errors = 0
    for idx, row in df.iterrows():
        # Check ranges
        for col in ['semantic_alignment', 'clarity', 'safety']:
            if col in df.columns:
                val = row[col]
                if not (0.0 <= val <= 1.0):
                    console.print(f"[red]Row {idx+2}:[/red] {col} value {val} out of range [0.0, 1.0]")
                    errors += 1
                    
    if errors > 0:
        console.print(f"[red]Found {errors} validation errors.[/red]")
        raise typer.Exit(code=1)
        
    console.print("[bold green]Validation Passed![/bold green] File adheres to HACS schema.")

@app.command()
def reliability(
    ratings: str = typer.Option(..., "--ratings", "-r", help="Path to ratings CSV"),
    domain: str = typer.Option("hacs", "--domain", "-d", help="Domain (hacs, smf, vision)"),
    criterion: str = typer.Option("semantic_alignment", "--criterion", "-c", help="Score column to analyze")
):
    """
    Calculate inter-rater reliability metrics (ICC, Krippendorff's Alpha).
    """
    try:
        df = load_ratings(ratings)
        matrix = create_reliability_matrix(df, criterion=criterion)
    except Exception as e:
        console.print(f"[red]Error processing data:[/red] {e}")
        raise typer.Exit(code=1)
        
    console.print(f"Analyzing reliability for [bold]{criterion}[/bold] with {matrix.shape[0]} items and {matrix.shape[1]} raters.")
    
    # Calculate ICC
    icc_val = calculate_icc(matrix, icc_type='icc2k')
    
    # Calculate Alpha (requires numpy array, transpose done inside function)
    # create_reliability_matrix returns subjects x raters
    # calculate_krippendorff_alpha expects subjects x raters (and handles transpose internally if needed? 
    # Wait, my docstring said input Rows=Subjects, Cols=Raters, but then I transposed it inside.
    # So I should pass it as is.
    alpha_val = calculate_krippendorff_alpha(matrix.values)
    
    table = Table(title=f"Reliability Metrics: {domain.upper()} - {criterion}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Interpretation", style="yellow")
    
    # Interpret ICC
    icc_interp = "Poor"
    if icc_val > 0.9: icc_interp = "Excellent"
    elif icc_val > 0.75: icc_interp = "Good"
    elif icc_val > 0.5: icc_interp = "Moderate"
    
    # Interpret Alpha
    alpha_interp = "Unreliable"
    if alpha_val > 0.8: alpha_interp = "Reliable"
    elif alpha_val > 0.667: alpha_interp = "Tentative"
    
    table.add_row("ICC(2,k)", f"{icc_val:.3f}", icc_interp)
    table.add_row("Krippendorff's Alpha", f"{alpha_val:.3f}", alpha_interp)
    
    console.print(table)

@app.command()
def validity(
    ratings: str = typer.Option(..., "--ratings", "-r", help="Path to ratings CSV to analyze correlations"),
    cols: str = typer.Option("semantic_alignment,clarity,creativity", "--cols", help="Comma-separated columns to correlate")
):
    """
    Check validity by calculating correlations between different rating criteria.
    (Construct/Discriminant Validity)
    """
    try:
        df = pd.read_csv(ratings)
        columns = [c.strip() for c in cols.split(',')]
        
        # Check if columns exist
        missing = [c for c in columns if c not in df.columns]
        if missing:
            console.print(f"[red]Error:[/red] Columns not found: {missing}")
            raise typer.Exit(code=1)
            
        # Calculate Correlation Matrix
        corr_matrix = df[columns].corr(method='pearson')
        
        console.print(f"[bold]Correlation Matrix (Pearson)[/bold] for: {columns}")
        
        table = Table(title="Convergent/Discriminant Validity")
        table.add_column("Metric", style="cyan")
        for c in columns:
            table.add_column(c, justify="right")
            
        for row_name in columns:
            row_vals = [row_name]
            for col_name in columns:
                val = corr_matrix.loc[row_name, col_name]
                style = "green" if val > 0.7 else "yellow" if val > 0.3 else "red"
                row_vals.append(f"[{style}]{val:.2f}[/{style}]")
            table.add_row(*row_vals)
            
        console.print(table)
        
        console.print("\n[bold]Interpretation Guide:[/bold]")
        console.print("- [green]> 0.7[/green]: Strong convergence (Convergent Validity)")
        console.print("- [yellow]0.3 - 0.7[/yellow]: Moderate correlation")
        console.print("- [red]< 0.3[/red]: Distinct constructs (Discriminant Validity)")

    except Exception as e:
        console.print(f"[red]Error during validity analysis:[/red] {e}")
        raise typer.Exit(code=1)

@app.command()
def report(
    study_id: str = typer.Option("study_001", "--id", help="Unique Study ID"),
    out: str = typer.Option("reports/research", "--out", help="Output directory")
):
    """
    Generate a standardized research report and data manifest.
    """
    out_dir = os.path.join(out, study_id)
    os.makedirs(out_dir, exist_ok=True)
    
    # Generate Manifest
    manifest = generate_data_manifest(
        file_paths={
            "ratings_schema": "datasets/hacs/ratings/schema.json",
            "protocol": "docs/research/protocol_overview.md"
        },
        version_info={"code": "0.1.0", "smf": "v1.0"}
    )
    
    with open(os.path.join(out_dir, "data_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        
    # Generate Dummy Summary
    summary = f"""# Research Report: {study_id}
    
## Metadata
- **Date**: {manifest['timestamp']}
- **Code Version**: {manifest['versions']['code']}

## Reliability
(Run `bench research reliability` to populate this)

## Validity
(Run `bench research validity` to populate this)

## Manifest
See `data_manifest.json` for file hashes.
"""
    with open(os.path.join(out_dir, "summary.md"), "w") as f:
        f.write(summary)
        
    console.print(f"[bold green]Report generated at:[/bold green] {out_dir}")
