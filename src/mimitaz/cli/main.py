import typer
import asyncio
from rich import print as rprint
from mimitaz.config import settings
from mimitaz.services.llm.factory import get_provider
from mimitaz.services.llm.provider import Message
from mimitaz.cli.ui import UI
from typing import Optional

# Initialize Typer App
app = typer.Typer(
    name="mimitaz",
    help="Minimalist AI CLI",
    no_args_is_help=False,
    add_completion=False,
)

config_app = typer.Typer(help="Manage configuration")
app.add_typer(config_app, name="config")

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    prompt: Optional[str] = typer.Argument(None, help="Input prompt"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
):
    """
    Mimitaz: The AI CLI (GLM Style).
    """
    if version:
        from rich import print as rprint
        rprint("[bold cyan]mimitaz[/] version 1.0.1")
        raise typer.Exit()

    if ctx.invoked_subcommand is not None:
        return

    # One-shot mode: mz "hello"
    if prompt:
        asyncio.run(run_processing(prompt))
    else:
        # Interactive mode: mz
        asyncio.run(run_repl())

# --- Core Logic ---

async def run_processing(prompt: str):
    """Run a single query and exit."""
    try:
        provider = get_provider()
        
        # 1. Print User Prompt
        UI.print_user_message(prompt)
        
        # 2. Stream Response
        messages = [Message(role="user", content=prompt)]
        
        try:
            api_key = settings.get_api_key() if settings.provider != "mock" else None
        except ValueError as e:
            UI.print_system_message(f"Configuration Error: {e}", type="error")
            UI.print_system_message("Run 'mz config set --provider openai --key sk-...'", type="info")
            return

        response_stream = provider.stream_chat(
            messages=messages,
            model=settings.model,
            api_key=api_key
        )
        
        # Bridge to sync world for Rich
        chunk_generator = [chunk async for chunk in response_stream]
        UI.print_stream(chunk_generator)
        
    except Exception as e:
        if settings.debug:
            import traceback
            traceback.print_exc()
        UI.print_system_message(f"Error: {str(e)}", type="error")

async def run_repl():
    """Interactive Loop."""
    try:
        provider = get_provider()
        api_key = settings.get_api_key() if settings.provider != "mock" else None
    except ValueError:
        UI.print_system_message("Missing API configuration.", type="error")
        UI.print_system_message("Run 'mz config set --provider <name> --key <key>'", type="info")
        return

    UI.print_banner()
    # UI.print_system_message(f"Active Provider: {settings.provider}")
    
    messages_history = []
    
    while True:
        try:
            UI.print_prompt()
            user_input = input() 
            
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input.strip():
                continue
                
            messages_history.append(Message(role="user", content=user_input))
            
            response_stream = provider.stream_chat(
                messages=messages_history, 
                model=settings.model, 
                api_key=api_key
            )
            
            # Streaming & Accumulation
            acc_response = ""
            chunk_generator = []
            async for chunk in response_stream:
                chunk_generator.append(chunk)
                acc_response += chunk.delta
            
            # Render
            UI.print_stream(chunk_generator)
            
            # Update History
            messages_history.append(Message(role="assistant", content=acc_response))
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
             UI.print_system_message(f"Error: {str(e)}", type="error")

# --- Config Commands ---

@config_app.command("set")
def config_set(
    provider: str = typer.Option(None, help="Provider name (openai, anthropic)"),
    key: str = typer.Option(None, help="API Key"),
    model: str = typer.Option(None, help="Model name"),
):
    """Update configuration settings."""
    env_path = settings.config_dir.parent / ".env" # Simplified for demo
    # Real implementation would update the .env file carefully
    rprint(f"[yellow]Configuration saved (Simulated):[/] Provider={provider}")
    # In a real app, we'd write to ~/.config/mimitaz/config.toml
    
if __name__ == "__main__":
    app()
