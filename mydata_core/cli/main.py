"""
Command-line interface for data generation.
"""

import json
import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from mydata_core.core.models import GenerationRequest
from mydata_core.core.generator import generate_and_insert

app = typer.Typer(help="MyData Synthetic Data Generation CLI")
console = Console()


@app.command()
def generate(
    schema_file: Path = typer.Option(
        ...,
        "--schema",
        "-s",
        help="Path to JSON schema file with generation specification",
        exists=True
    ),
    db_type: Optional[str] = typer.Option(
        None,
        "--db-type",
        "-t",
        help="Database type (postgresql or mongodb). Overrides schema file."
    ),
    connection_uri: Optional[str] = typer.Option(
        None,
        "--uri",
        "-u",
        help="Database connection URI. Overrides schema file."
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output"
    )
):
    """
    Generate and insert synthetic data from a JSON schema file.
    
    Example schema file:
    {
        "database_type": "postgresql",
        "connection_uri": "postgresql://user:pass@localhost/dbname",
        "entities": [
            {
                "name": "users",
                "records": 100,
                "fields": [
                    {"name": "id", "logical_type": "integer", "constraints": {"primary_key": true, "auto_increment": true}},
                    {"name": "name", "logical_type": "name"},
                    {"name": "email", "logical_type": "email", "constraints": {"unique": true}}
                ]
            }
        ]
    }
    """
    try:
        # Load schema file
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)
        
        # Override database type and connection URI if provided
        if db_type:
            schema_data['database_type'] = db_type
        if connection_uri:
            schema_data['connection_uri'] = connection_uri
        
        # Parse request
        request = GenerationRequest(**schema_data)
        
        console.print(f"\n[bold cyan]Starting data generation...[/bold cyan]")
        console.print(f"Database type: [yellow]{request.database_type}[/yellow]")
        console.print(f"Entities: [yellow]{len(request.entities)}[/yellow]")
        console.print(f"Total records to generate: [yellow]{sum(e.records for e in request.entities)}[/yellow]\n")
        
        # Generate and insert data
        with console.status("[bold green]Generating and inserting data..."):
            response = generate_and_insert(request)
        
        # Display results
        if response.success:
            console.print(f"\n[bold green]✓ Success![/bold green]")
            console.print(f"\n{response.message}\n")
            
            # Create results table
            table = Table(title="Insertion Results", show_header=True, header_style="bold magenta")
            table.add_column("Entity", style="cyan")
            table.add_column("Records Inserted", justify="right", style="green")
            
            for entity_name, count in response.inserted_counts.items():
                table.add_column_row = table.add_row(entity_name, str(count))
            
            console.print(table)
            
            if verbose and response.errors:
                console.print("\n[bold yellow]Warnings:[/bold yellow]")
                for error in response.errors:
                    console.print(f"  • {error}")
        else:
            console.print(f"\n[bold red]✗ Failed![/bold red]")
            console.print(f"\n{response.message}\n")
            
            if response.errors:
                console.print("[bold red]Errors:[/bold red]")
                for error in response.errors:
                    console.print(f"  • {error}")
            
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def validate(
    schema_file: Path = typer.Option(
        ...,
        "--schema",
        "-s",
        help="Path to JSON schema file to validate",
        exists=True
    )
):
    """Validate a schema file without generating data."""
    try:
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)
        
        request = GenerationRequest(**schema_data)
        
        console.print("[bold green]✓ Schema is valid![/bold green]\n")
        console.print(f"Database type: [yellow]{request.database_type}[/yellow]")
        console.print(f"Entities: [yellow]{len(request.entities)}[/yellow]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Entity", style="cyan")
        table.add_column("Fields", justify="right", style="green")
        table.add_column("Records", justify="right", style="yellow")
        
        for entity in request.entities:
            table.add_row(entity.name, str(len(entity.fields)), str(entity.records))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]✗ Invalid schema:[/bold red] {str(e)}")
        raise typer.Exit(1)


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
