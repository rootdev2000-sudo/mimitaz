import typer
import asyncio
import sys
from rich import print as rprint
from mimitaz.config import settings
from mimitaz.services.llm.factory import get_provider
from mimitaz.services.llm.provider import Message
from mimitaz.cli.ui import UI
from mimitaz.cli.config_cmd import config_app
from mimitaz.cli.token_cmd import token_app
from typing import Optional, List

# Core Typer App
app = typer.Typer(
    name="mimitaz",
    help="Minimalist AI CLI",
    no_args_is_help=False,
    add_completion=False,
)

app.add_typer(config_app, name="config")
app.add_typer(token_app, name="token")

# --- Commands ---

@app.command("chat")
def chat_command(
    ctx: typer.Context,
    prompt: List[str] = typer.Argument(None, help="Input prompt"),
):
    """Internal command to handle one-shot queries."""
    text = " ".join(prompt).strip()
    if text:
        asyncio.run(run_processing(text))
    else:
        asyncio.run(run_repl())

# --- Callback ---
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
):
    if version:
        rprint("[bold cyan]mimitaz[/] version 1.0.1")
        raise typer.Exit()
    
    if settings.debug or debug:
        settings.debug = True

    # Note: This callback is only reached if a subcommand is NOT invoked,
    # OR if invoke_without_command is True.
    # However, due to our sys.argv shim below, we mostly route to 'chat' or 'config'.
    pass

# --- Core Logic ---

async def run_processing(prompt: str):
    """Run a single query and exit."""
    try:
        provider = get_provider()
        UI.print_user_message(prompt)
        messages = [Message(role="user", content=prompt)]
        
        try:
            api_key = settings.get_api_key()
        except ValueError as e:
            UI.print_system_message(f"{e}", type="error")
            return

        response_stream = provider.stream_chat(
            messages=messages,
            model=settings.model,
            api_key=api_key
        )
        
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
        api_key = settings.get_api_key()
    except ValueError as e:
        UI.print_system_message(f"{e}", type="error")
        return

    UI.print_banner()
    messages_history = []
    
    while True:
        try:
            UI.print_prompt()
            user_input = input() 
            messages_history.append(Message(role="user", content=user_input))
            
            response_stream = provider.stream_chat(
                messages=messages_history, 
                model=settings.model, 
                api_key=api_key
            )
            
            acc_response = ""
            chunk_generator = []
            async for chunk in response_stream:
                chunk_generator.append(chunk)
                acc_response += chunk.delta
            
            UI.print_stream(chunk_generator)
            messages_history.append(Message(role="assistant", content=acc_response))
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
             UI.print_system_message(f"Error: {str(e)}", type="error")

def entry_point():
    """
    Manual dispatch shim to support 'mim <query>' syntax alongside subcommands.
    """
    args = sys.argv[1:]

    # Early exit for no args -> REPL
    if not args:
        # Route to 'chat' without args -> REPL
        sys.argv = [sys.argv[0], "chat"]
        app()
        return

    # Check for known commands or flags
    first_arg = args[0]
    known_commands = ["config", "chat"]
    known_flags = ["--help", "--version", "-v"]

    if first_arg in known_commands or first_arg in known_flags:
        # Standard Typer behavior
        app()
    else:
        # Treat as implicit 'chat' command
        # Transform: mim "hello" -> mim chat "hello"
        # We explicitly pass the args to avoid sys.argv ambiguity
        app(args=["chat"] + args)

if __name__ == "__main__":
    entry_point()
