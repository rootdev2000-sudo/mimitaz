from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.live import Live
from rich.style import Style
from rich.panel import Panel

# GLM-style minimalist theme
glm_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "user": "bold cyan",
    "assistant": "white",
    "code.hilite": "bold magenta",
})

console = Console(theme=glm_theme)

class UI:
    """
    Minimalist GLM-style UI Renderer.
    "Invisible" interface - just text and content.
    """
    
    @staticmethod
    def print_banner():
        """Prints the startup banner."""
        banner = """
 ███╗   ███╗██╗███╗   ███╗
 ████╗ ████║██║████╗ ████║
 ██╔████╔██║██║██╔████╔██║
 ██║╚██╔╝██║██║██║╚██╔╝██║
 ██║ ╚═╝ ██║██║██║ ╚═╝ ██║
 ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝
        """
        console.print(banner, style="gradient", justify="left")
        console.print("[dim]  v1.0.1 • neural link active[/]", justify="left")
        console.print()

    @staticmethod
    def print_prompt():
        """Prints the user prompt marker."""
        console.print()
        console.print(">", style="user", end=" ")

    @staticmethod
    def print_user_message(content: str):
        """Retroactively prints the user message if we are replaying history."""
        console.print(">", style="user", end=" ")
        console.print(content)

    @staticmethod
    def print_system_message(content: str, type: str = "info"):
        """Prints a transient or helpful system message."""
        console.print(f"[{type}]>>> {content}[/]")

    @staticmethod
    def print_stream(generator):
        """
        Consumes a StreamChunk iterator and renders it live.
        """
        console.print() # Spacing
        
        acc_text = ""
        # vertical_overflow="visible" is key for long responses
        with Live(console=console, refresh_per_second=12, vertical_overflow="visible") as live:
            for chunk in generator:
                if chunk.delta:
                    acc_text += chunk.delta
                    live.update(Markdown(acc_text))
        
        console.print() # Final spacing
