import typer
import json
from rich import print as rprint
from mimitaz.cli.config_cmd import save_config_file, load_config_file, CONFIG_FILE
from mimitaz.config import settings

token_app = typer.Typer(help="Manage authentication tokens (GLM Style)")

@token_app.command("set")
def token_set(
    key: str = typer.Argument(..., help="The API Key"),
    provider: str = typer.Option("glm", help="The provider for this key (glm, openai, anthropic)"),
):
    """
    Set an Authentication Token.
    Defaults to setting the GLM (ZhipuAI) key if no provider is specified.
    """
    config_key = ""
    if provider in ("glm", "zhipu"):
        config_key = "zhipu.api_key"
        # If setting GLM key, logically switch to GLM provider too for convenience
        save_config_file({"provider": "glm", "model": "glm-4"})
        rprint("[green]✓ Switched to GLM-4[/green]")
    elif provider == "openai":
        config_key = "openai.api_key"
    elif provider == "anthropic":
        config_key = "anthropic.api_key"
    else:
        rprint(f"[red]Unknown provider: {provider}[/red]")
        raise typer.Exit(1)
        
    save_config_file({config_key: key})
    
    masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "********"
    rprint(f"[green]✓ Token set for {provider}:[/green] {masked_key}")

@token_app.command("show")
def token_show(
    provider: str = typer.Option(None, help="Provider to show token for (default: active)"),
):
    """
    View current token (masked).
    """
    target = provider or settings.provider
    if target == "mock":
        rprint("[yellow]Active provider is 'mock' (no token required).[/yellow]")
        return

    # Get from Settings (Source of Truth: Env + Config + Defaults)
    val = None
    if target == "openai":
        val = settings.openai_api_key
    elif target == "anthropic":
        val = settings.anthropic_api_key
    elif target in ("glm", "zhipu"):
        val = settings.zhipu_api_key
        
    if val:
        raw = val.get_secret_value()
        masked = f"{raw[:4]}...{raw[-4:]}" if len(raw) > 8 else "********"
        rprint(f"Current token for [bold cyan]{target}[/bold cyan]: {masked}")
    else:
        rprint(f"[yellow]No token found for {target}.[/yellow]")

@token_app.command("clear")
def token_clear(
    provider: str = typer.Option("glm", help="Provider to clear token for"),
):
    """
    Clear stored token.
    """
    # Map to config keys
    key_map = {
        "openai": "openai.api_key",
        "anthropic": "anthropic.api_key",
        "glm": "zhipu.api_key",
        "zhipu": "zhipu.api_key"
    }
    
    target_key = key_map.get(provider)
    if not target_key:
        rprint(f"[red]Unknown provider: {provider}[/red]")
        return

    # Load, Modify, Save
    data = load_config_file()
    if target_key in data:
        del data[target_key]
        CONFIG_FILE.write_text(json.dumps(data, indent=2))
        rprint(f"[green]✓ Token for {provider} cleared from config.[/green]")
    else:
        rprint(f"[yellow]No stored token found for {provider}.[/yellow]")
