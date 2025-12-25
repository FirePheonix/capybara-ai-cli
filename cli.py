#!/usr/bin/env python3
import os
import subprocess
import yaml
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich import box
from rich.console import Console
from openai import OpenAI
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from plugins.keyboard_sound import toggle_keyboard_sounds, is_keyboard_sounds_active, start_keyboard_sounds, stop_keyboard_sounds
from plugins.soundpack_manager import discover_soundpacks, format_soundpack_list, get_soundpack_by_index, get_soundpack_by_name

console = Console()
session = PromptSession(history=FileHistory(".capybara_history"))

# Global variable to store current soundpack
current_soundpack = None

def load_config():
    # Try .env file first
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"').strip("'")
                    os.environ[key.strip()] = value
    
    # Check environment variable
    if os.environ.get("OPENAI_API_KEY"):
        return {"openai_api_key": os.environ["OPENAI_API_KEY"]}
    
    # Try config.yaml
    try:
        with open("config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        api_key = input("Enter OpenAI API Key: ").strip()
        config = {"openai_api_key": api_key}
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)
        return config

config = load_config()
client = OpenAI(api_key=config["openai_api_key"])

class HybridCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("?"):
            yield Completion(
                "ask",
                start_position=-1,
                display="?Ask Capybara anything"
            )
        elif text.startswith("!"):
            partial = text[1:]
            for cmd in ["explain", "git", "find", "readme", "sounds", "vibes", "soundpacks", "packs", "select", "help"]:
                if cmd.startswith(partial):
                    yield Completion(
                        cmd[len(partial):],
                        start_position=-len(partial),
                        display=f"!{cmd} - AI helper"
                    )
        else:
            yield from PathCompleter().get_completions(document, complete_event)

def explain_command(cmd: str) -> str:
    prompt = f"Explain this shell command in one line:\n{cmd}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def get_current_dir() -> str:
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    return cwd.replace(home, "~")

def execute_command(cmd: str):
    global current_soundpack
    try:
        if cmd.startswith("?"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": cmd[1:]}],
                temperature=0.7,
                max_tokens=1000
            )
            console.print(Panel.fit(
                response.choices[0].message.content,
                title="Capybara",
                border_style="blue",
                width=80
            ))
        elif cmd.startswith("!explain"):
            explanation = explain_command(cmd[8:])
            console.print(Panel.fit(
                explanation,
                title="Explanation",
                border_style="yellow",
                width=80
            ))
        elif cmd.startswith("!git"):
            from plugins.git_helper import handle_git
            suggestion = handle_git(cmd[4:].split())
            console.print(Panel.fit(
                suggestion,
                title="Git Suggestion",
                border_style="green",
                width=80
            ))
        elif cmd.startswith("!find"):
            from plugins.file_search import handle_find
            search_cmd = handle_find(cmd[5:])
            console.print(Panel.fit(
                search_cmd,
                title="File Search",
                border_style="cyan",
                width=80
            ))
        elif cmd.startswith("!readme"):
            from plugins.readme_generator import handle_readme_generation
            console.print("[yellow]Generating README... This may take a moment.[/]")
            readme_content = handle_readme_generation(cmd[7:].split())
            console.print(Panel(
                Markdown(readme_content),
                title="Generated README",
                border_style="green",
                width=100
            ))
            # Ask if user wants to save
            save = input("\nSave to README.md? (y/n): ").strip().lower()
            if save == 'y':
                with open("README.md", "w", encoding="utf-8") as f:
                    f.write(readme_content)
                console.print("[green]✓ Saved to README.md[/]")
        elif cmd.startswith("cd"):
            try:
                path = os.path.expanduser(cmd[3:].strip() or "~")
                os.chdir(path)
                return
            except Exception as e:
                console.print(f"[red]Error:[/] {e}")
                return

        elif cmd == "!sounds" or cmd == "!vibes":
            # Toggle keyboard sounds with last selected soundpack
            sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
            
            if is_keyboard_sounds_active():
                stop_keyboard_sounds()
                console.print(Panel.fit(
                    "[yellow]🔇 Keyboard sounds disabled[/yellow]",
                    title="Mechanical Keyboard Vibes",
                    border_style="yellow",
                    width=80
                ))
            else:
                # Use current soundpack or default to sounds dir
                pack_dir = current_soundpack if current_soundpack else sounds_dir
                is_active = start_keyboard_sounds(soundpack_dir=str(pack_dir), volume=0.3)
                if is_active:
                    pack_name = Path(pack_dir).name if current_soundpack else "default"
                    console.print(Panel.fit(
                        f"[green]🔊 Keyboard sounds enabled![/green]\n[dim]Soundpack: {pack_name}[/dim]",
                        title="Mechanical Keyboard Vibes",
                        border_style="green",
                        width=80
                    ))
                else:
                    console.print(Panel.fit(
                        "[red]Could not start keyboard sounds. Install dependencies: py -m pip install pygame pynput[/red]",
                        title="Error",
                        border_style="red",
                        width=80
                    ))
        
        elif cmd == "!soundpacks" or cmd == "!packs":
            # List available soundpacks
            sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
            soundpacks = discover_soundpacks(sounds_dir)
            soundpack_list = format_soundpack_list(soundpacks)
            console.print(Panel(
                soundpack_list,
                title="🎹 Keyboard Soundpacks",
                border_style="cyan",
                width=100
            ))
            if soundpacks:
                console.print("[dim]Use [bold]!select <number|name>[/bold] to choose a soundpack[/dim]")
        
        elif cmd.startswith("!select "):
            # Select a soundpack
            sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
            soundpacks = discover_soundpacks(sounds_dir)
            
            selector = cmd[8:].strip()
            selected_pack = None
            
            # Try to parse as number
            try:
                index = int(selector)
                selected_pack = get_soundpack_by_index(soundpacks, index)
            except ValueError:
                # Try as name
                selected_pack = get_soundpack_by_name(soundpacks, selector)
            
            if selected_pack:
                current_soundpack = selected_pack
                was_active = is_keyboard_sounds_active()
                
                # Restart if already active
                if was_active:
                    stop_keyboard_sounds()
                    start_keyboard_sounds(soundpack_dir=str(selected_pack), volume=0.3)
                
                console.print(Panel.fit(
                    f"[green]✓ Selected soundpack: {selected_pack.name}[/green]\n[dim]Use !sounds to {('disable' if was_active else 'enable')} keyboard sounds[/dim]",
                    title="Soundpack Selected",
                    border_style="green",
                    width=80
                ))
            else:
                console.print(Panel.fit(
                    f"[red]Soundpack '{selector}' not found. Use !soundpacks to see available options.[/red]",
                    title="Error",
                    border_style="red",
                    width=80
                ))
        elif cmd == "!help":
            console.print(Panel.fit(
                Text.from_markup("""
[b]COMMAND HELP[/b]
[cyan]?[query][/]         - Ask Capybara anything
[yellow]!explain [cmd][/] - Explain shell commands
[green]!git [action][/]     - Smart Git helper
[magenta]!find [query][/]    - Natural language file search
[blue]!readme [path][/]   - Generate README for a repository
[bold green]!sounds / !vibes[/] - Toggle keyboard sounds
[bold cyan]!soundpacks[/]      - List available soundpacks
[bold cyan]!select <name>[/]   - Select a soundpack
[dim]exit/quit - Exit shell"""),
                title="Help",
                border_style="blue",
                width=80
            ))

        else:
            result = subprocess.run(
                cmd, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(f"[red]{result.stderr}[/]")
            if result.returncode != 0:
                fix_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Fix this shell error concisely:\nCommand: {cmd}\nError: {result.stderr}\nProvide ONLY the corrected command."}],
                    temperature=0.7,
                    max_tokens=500
                )
                console.print(Panel.fit(
                    fix_response.choices[0].message.content.strip(),
                    title="Try This",
                    border_style="red",
                    width=80
                ))
    except Exception as e:
        console.print(Panel.fit(
            f"Error: {str(e)}\nType [b]!help[/] for assistance",
            border_style="red",
            width=80
        ))

def run_cli():
    try:
        with open("ascii.txt", "r", encoding="utf-8") as f:
            capybara_art = f.read()
    except FileNotFoundError:
        capybara_art = "🌿 Capybara CLI 🌿"
    
    console.print(Panel.fit(
        Text(capybara_art + "\n\n[bold green]Capybara Smart CLI[/] [dim](type !help for commands)", style="cyan"),
        title="CapybaraCLI",
        border_style="bright_blue",
        subtitle=f"{get_current_dir()}",
        subtitle_align="right"
    ))

    while True:
        try:
            user_input = session.prompt(
                f"CapybaraCLI {get_current_dir()}> ",
                completer=HybridCompleter(),
                auto_suggest=AutoSuggestFromHistory()
            ).strip()

            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                break

            execute_command(user_input)

        except KeyboardInterrupt:
            console.print(Panel.fit(
                Text.from_markup("\n[yellow]Use 'exit' to quit[/]")
            ))
            continue

def render_markdown(content: str, width: int = 80) -> Panel:
    """Render markdown content with proper formatting"""
    return Panel(
        Markdown(content.strip()),
        border_style="blue",
        box=box.ROUNDED,
        width=min(width, os.get_terminal_size().columns - 4),
        padding=(1, 2)
    )

if __name__ == "__main__":
    run_cli()
