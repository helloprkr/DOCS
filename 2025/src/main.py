import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import os
from dotenv import load_dotenv
from pathlib import Path

from utils import load_config, setup_logging, ensure_directory
from note_generator import NoteGenerator
from variable_processor import VariableProcessor
from scheduler import NoteScheduler

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

def setup_environment():
    """Set up the application environment."""
    load_dotenv()
    config = load_config()
    logger = setup_logging(config)
    
    # Ensure required directories exist
    ensure_directory(config["notes"]["output_directory"])
    ensure_directory(os.path.dirname(config["logging"]["file"]))
    ensure_directory("data")  # For variable persistence
    
    return config, logger

@app.command()
def generate(
    analyze: Optional[str] = typer.Option(None, help="Analysis content"),
    strategize: Optional[str] = typer.Option(None, help="Strategy content"),
    pre_problem_solve: Optional[str] = typer.Option(None, help="Pre-problem solving content"),
    outlining: Optional[str] = typer.Option(None, help="Outline content"),
    outcome: Optional[str] = typer.Option(None, help="Outcome content"),
    end_state: Optional[str] = typer.Option(None, help="End state content")
):
    """Generate a note with optional content."""
    try:
        config, logger = setup_environment()
        
        # Initialize components
        variable_processor = VariableProcessor(logger)
        note_generator = NoteGenerator(config, logger)
        
        # Add provided content to variables
        variables = {
            "analyze": analyze,
            "strategize": strategize,
            "pre_problem_solve": pre_problem_solve,
            "outlining": outlining,
            "outcome": outcome,
            "end_state": end_state
        }
        
        # Add non-None variables
        for name, value in variables.items():
            if value is not None:
                variable_processor.add_variable(name, value)
            
        # Generate note
        note_content = note_generator.generate_daily_note(
            variable_processor.get_context(),
            variable_processor.get_tasks()
        )
        
        console.print("[green]Note generated successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error generating note: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def add_task(
    description: str = typer.Argument(..., help="Task description"),
    completed_today: bool = typer.Option(False, "--today", help="Mark as completed today"),
    completed_later: bool = typer.Option(False, "--later", help="Mark as completed later"),
    decided_against: bool = typer.Option(False, "--against", help="Mark as decided against")
):
    """Add a task to the current note."""
    try:
        config, logger = setup_environment()
        variable_processor = VariableProcessor(logger)
        
        status = {
            "completed_today": completed_today,
            "completed_later": completed_later,
            "decided_against": decided_against
        }
        
        variable_processor.add_task(description, status)
        console.print("[green]Task added successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error adding task: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command(name="clear")
def clear_all():
    """Clear all tasks and variables."""
    try:
        config, logger = setup_environment()
        variable_processor = VariableProcessor(logger)
        variable_processor.clear()
        console.print("[green]All data cleared successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error clearing data: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def list_tasks():
    """List all current tasks."""
    try:
        config, logger = setup_environment()
        variable_processor = VariableProcessor(logger)
        tasks = variable_processor.get_tasks()
        
        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return
            
        table = Table(title="Current Tasks")
        table.add_column("Index", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Status", style="green")
        
        for i, task in enumerate(tasks):
            status = []
            if task.get("completed_today"):
                status.append("Completed Today")
            elif task.get("completed_later"):
                status.append("Completed Later")
            elif task.get("decided_against"):
                status.append("Decided Against")
            else:
                status.append("Pending")
                
            table.add_row(str(i), task["description"], ", ".join(status))
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing tasks: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def start_scheduler():
    """Start the note generation scheduler."""
    try:
        config, logger = setup_environment()
        
        def generate_scheduled_note():
            variable_processor = VariableProcessor(logger)
            note_generator = NoteGenerator(config, logger)
            note_generator.generate_daily_note(
                variable_processor.get_context(),
                variable_processor.get_tasks()
            )
            
        scheduler = NoteScheduler(config, logger, generate_scheduled_note)
        
        console.print(f"[green]Starting scheduler...[/green]")
        console.print(f"Will generate notes daily at {config['automation']['schedule_time']} "
                     f"{config['automation']['timezone']}")
        
        scheduler.start()
        
    except Exception as e:
        console.print(f"[red]Error starting scheduler: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def status():
    """Show the current status of the note generation system."""
    try:
        config, logger = setup_environment()
        variable_processor = VariableProcessor(logger)
        
        table = Table(title="Note Generation System Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        
        # Check configuration
        table.add_row("Configuration", "Loaded" if config else "Not loaded")
        
        # Check directories
        notes_dir = os.path.exists(config["notes"]["output_directory"])
        data_dir = os.path.exists("data")
        table.add_row("Notes Directory", "Exists" if notes_dir else "Missing")
        table.add_row("Data Directory", "Exists" if data_dir else "Missing")
        
        # Check API configuration
        api_provider = config["ai"]["provider"]
        api_key = bool(config["ai"][f"{api_provider}_api_key"])
        table.add_row("AI Provider", f"{api_provider} ({'Configured' if api_key else 'Not configured'})")
        
        # Check automation status
        table.add_row("Automation", "Enabled" if config["automation"]["enabled"] else "Disabled")
        
        # Check tasks
        tasks = variable_processor.get_tasks()
        table.add_row("Active Tasks", str(len(tasks)))
        
        # Check recent notes
        notes_path = Path(config["notes"]["output_directory"])
        recent_notes = list(notes_path.glob("*.md"))
        table.add_row("Recent Notes", str(len(recent_notes)))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error checking status: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
