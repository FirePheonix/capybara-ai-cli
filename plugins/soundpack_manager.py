"""
Soundpack selector and manager for keyboard sounds
"""
import json
from pathlib import Path
from typing import List, Dict, Optional


class SoundpackInfo:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.full_name = None
        self.sound_count = 0
        self.includes_numpad = False
        
        # Try to load config.json
        config_file = path / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.full_name = config.get('name', self.name)
                    self.sound_count = len(config.get('defines', {}))
                    self.includes_numpad = config.get('includes_numpad', False)
            except Exception:
                pass
        
        # Count sound files if config not available
        if self.sound_count == 0:
            sound_extensions = ['.wav', '.mp3', '.ogg']
            for ext in sound_extensions:
                self.sound_count += len(list(path.glob(f'*{ext}')))


def discover_soundpacks(base_dir: str) -> List[SoundpackInfo]:
    """Discover all available soundpacks in the base directory."""
    base_path = Path(base_dir)
    soundpacks = []
    
    if not base_path.exists():
        return soundpacks
    
    # Check direct subdirectories for soundpacks
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it has config.json or sound files
            has_config = (item / "config.json").exists()
            has_sounds = any(item.glob('*.wav')) or any(item.glob('*.ogg')) or any(item.glob('*.mp3'))
            
            if has_config or has_sounds:
                soundpacks.append(SoundpackInfo(item))
    
    # Also check Soundpacks subdirectory
    soundpacks_dir = base_path / "Soundpacks"
    if soundpacks_dir.exists():
        for item in soundpacks_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                has_config = (item / "config.json").exists()
                has_sounds = any(item.glob('*.wav')) or any(item.glob('*.ogg')) or any(item.glob('*.mp3'))
                
                if has_config or has_sounds:
                    soundpacks.append(SoundpackInfo(item))
    
    return soundpacks


def format_soundpack_list(soundpacks: List[SoundpackInfo]) -> str:
    """Format soundpack list for display."""
    if not soundpacks:
        return "[yellow]No soundpacks found. Place soundpacks in the 'sounds/' or 'sounds/Soundpacks/' directory.[/yellow]"
    
    lines = ["[bold cyan]Available Soundpacks:[/bold cyan]\n"]
    
    for i, pack in enumerate(soundpacks, 1):
        name = pack.full_name or pack.name
        sounds = f"{pack.sound_count} sounds"
        lines.append(f"[green]{i}.[/green] [bold]{name}[/bold]")
        lines.append(f"   [dim]{pack.path.name} - {sounds}[/dim]")
    
    lines.append(f"\n[dim]Total: {len(soundpacks)} soundpacks[/dim]")
    return "\n".join(lines)


def get_soundpack_by_index(soundpacks: List[SoundpackInfo], index: int) -> Optional[Path]:
    """Get soundpack path by index (1-based)."""
    if 1 <= index <= len(soundpacks):
        return soundpacks[index - 1].path
    return None


def get_soundpack_by_name(soundpacks: List[SoundpackInfo], name: str) -> Optional[Path]:
    """Get soundpack path by name (case-insensitive partial match)."""
    name_lower = name.lower()
    
    # Try exact match first
    for pack in soundpacks:
        if pack.name.lower() == name_lower or (pack.full_name and pack.full_name.lower() == name_lower):
            return pack.path
    
    # Try partial match
    for pack in soundpacks:
        if name_lower in pack.name.lower() or (pack.full_name and name_lower in pack.full_name.lower()):
            return pack.path
    
    return None
