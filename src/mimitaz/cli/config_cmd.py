import typer
import json
from pathlib import Path
from rich import print as rprint
from mimitaz.config import settings

# Initialize Typer Sub-App for Config
config_app = typer.Typer(help="Manage configuration (GLM Style)")

CONFIG_FILE = Path.home() / ".mimitaz_config.json"

def load_config_file() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception:
        return {}

def save_config_file(data: dict):
    # Merge with existing
    current = load_config_file()
    current.update(data)
    CONFIG_FILE.write_text(json.dumps(current, indent=2))

@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="The config key (e.g., openai.api_key)"),
    value: str = typer.Argument(..., help="The value to set"),
):
    """
    Set a configuration value.
    Example: mim config set openai.api_key sk-12345...
    """
    # Simple nested key handling for flat "section.key" style
    save_config_file({key: value})
    rprint(f"[green]✓ Config updated:[/green] {key} = [dim]********[/dim]")

@config_app.command("list")
def config_list():
    """List current configuration."""
    data = load_config_file()
    if not data:
        rprint("[dim]No configuration found.[/dim]")
        return
    
    rprint(f"[bold]Configuration ({CONFIG_FILE}):[/bold]")
    for k, v in data.items():
        # Obfuscate keys
        if "key" in k.lower():
            v = f"{v[:4]}...{v[-4:]}" if len(v) > 8 else "********"
        rprint(f"  [cyan]{k}[/cyan] = {v}")

@config_app.command("get")
def config_get(key: str):
    """Get a specific config value."""
    data = load_config_file()
    val = data.get(key)
    if val:
        rprint(val)
    else:
        rprint(f"[red]Key '{key}' not found.[/red]")
