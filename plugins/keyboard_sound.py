"""
Mechanical Keyboard Sound Effect Module
Inspired by rustyvibes - plays sound effects on keypresses
Supports OGG, WAV, and MP3 files using pygame-ce
"""
import threading
import queue
import random
import json
from pathlib import Path
from typing import Optional, Dict
import time

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

# Use pygame-ce for audio (supports OGG, WAV, MP3)
try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.set_num_channels(32)
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
except Exception as e:
    print(f"Warning: pygame mixer init failed: {e}")
    PYGAME_AVAILABLE = False


class KeyboardSoundPlayer:
    def __init__(self, soundpack_dir: Optional[str] = None, volume: float = 0.5):
        """
        Initialize the keyboard sound player.
        
        Args:
            soundpack_dir: Path to directory containing sound files
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self.soundpack_dir = Path(soundpack_dir) if soundpack_dir else None
        self.is_active = False
        self.listener = None
        self.sound_queue = queue.Queue(maxsize=10)
        self.worker_thread = None
        self.pressed_keys = set()
        self.keycode_map: Dict[int, str] = {}
        self.sound_cache = {}  # pygame Sound objects
        self.sound_files = []  # For random selection
        
        # Load sounds if soundpack directory exists
        if self.soundpack_dir and self.soundpack_dir.exists():
            self._load_sounds()
    
    def _load_sounds(self):
        """Load sound files from the soundpack directory."""
        if not PYGAME_AVAILABLE:
            print("⚠️  pygame-ce not available. Install with: pip install pygame-ce")
            return
        
        # Check for config.json
        config_file = self.soundpack_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    defines = config.get('defines', {})
                    
                    # Load sounds according to keycode mapping
                    for keycode, sound_file in defines.items():
                        try:
                            keycode_int = int(keycode)
                            sound_path = self.soundpack_dir / sound_file
                            if sound_path.exists():
                                # Load with pygame (supports OGG, WAV, MP3)
                                sound = pygame.mixer.Sound(str(sound_path))
                                sound.set_volume(self.volume)
                                self.sound_cache[keycode_int] = sound
                                self.keycode_map[keycode_int] = sound_file
                        except Exception:
                            pass
                    
                    print(f"✓ Loaded: {config.get('name', 'Unknown')} ({len(self.sound_cache)} sounds)")
                    return
            except Exception as e:
                print(f"Warning: Could not load config.json: {e}")
        
        # Fallback: Load all sound files
        sound_extensions = ['.wav', '.mp3', '.ogg']
        for ext in sound_extensions:
            for sound_file in self.soundpack_dir.glob(f'*{ext}'):
                try:
                    sound = pygame.mixer.Sound(str(sound_file))
                    sound.set_volume(self.volume)
                    self.sound_files.append(sound)
                except:
                    pass
        
        if self.sound_files:
            print(f"✓ Loaded {len(self.sound_files)} sounds")
    
    def _sound_worker(self):
        """Worker thread that plays sounds from the queue."""
        while self.is_active:
            try:
                sound_info = self.sound_queue.get(timeout=0.5)
                if sound_info and PYGAME_AVAILABLE:
                    keycode = sound_info if isinstance(sound_info, int) else None
                    
                    # Try keycode-specific sound first
                    if keycode and keycode in self.sound_cache:
                        sound = self.sound_cache[keycode]
                    elif self.sound_files:
                        sound = random.choice(self.sound_files)
                    else:
                        continue
                    
                    # Play with pygame
                    try:
                        sound.play()
                    except Exception:
                        pass
            except queue.Empty:
                continue
            except Exception:
                pass
    
    def _on_press(self, key):
        """Callback for key press events."""
        try:
            # Get keycode
            if hasattr(key, 'vk'):
                key_id = key.vk
                keycode = key.vk
            elif hasattr(key, 'char') and key.char:
                key_id = ord(key.char)
                keycode = ord(key.char)
            else:
                key_id = str(key)
                keycode = None
            
            # Only play on new press (not held)
            if key_id not in self.pressed_keys:
                self.pressed_keys.add(key_id)
                try:
                    self.sound_queue.put_nowait(keycode if keycode else True)
                except queue.Full:
                    pass
        except Exception:
            pass
    
    def _on_release(self, key):
        """Callback for key release events."""
        try:
            if hasattr(key, 'vk'):
                key_id = key.vk
            elif hasattr(key, 'char') and key.char:
                key_id = ord(key.char)
            else:
                key_id = str(key)
            
            self.pressed_keys.discard(key_id)
        except Exception:
            pass
    
    def start(self):
        """Start listening for keyboard events."""
        if not PYNPUT_AVAILABLE:
            print("⚠️  pynput not available. Install with: pip install pynput")
            return False
        
        if not PYGAME_AVAILABLE:
            print("⚠️  pygame-ce not available. Install with: pip install pygame-ce")
            return False
        
        if not self.sound_cache and not self.sound_files:
            print("⚠️  No sounds loaded.")
            return False
        
        if self.is_active:
            return True
        
        self.is_active = True
        
        # Start sound worker thread
        self.worker_thread = threading.Thread(target=self._sound_worker, daemon=True)
        self.worker_thread.start()
        
        # Start keyboard listener
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        
        return True
    
    def stop(self):
        """Stop listening for keyboard events."""
        self.is_active = False
        
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
            self.worker_thread = None
    
    def set_volume(self, volume: float):
        """Set the volume level (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sound_cache.values():
            sound.set_volume(self.volume)
        for sound in self.sound_files:
            sound.set_volume(self.volume)
    
    def is_running(self) -> bool:
        """Check if the player is running."""
        return self.is_active


# Global instance
_global_player: Optional[KeyboardSoundPlayer] = None


def start_keyboard_sounds(soundpack_dir: Optional[str] = None, volume: float = 0.3):
    """Start playing keyboard sounds globally."""
    global _global_player
    
    if _global_player and _global_player.is_running():
        return True
    
    _global_player = KeyboardSoundPlayer(soundpack_dir, volume)
    return _global_player.start()


def stop_keyboard_sounds():
    """Stop playing keyboard sounds globally."""
    global _global_player
    
    if _global_player:
        _global_player.stop()
        _global_player = None


def toggle_keyboard_sounds(soundpack_dir: Optional[str] = None, volume: float = 0.3):
    """Toggle keyboard sounds on/off."""
    global _global_player
    
    if _global_player and _global_player.is_running():
        stop_keyboard_sounds()
        return False
    else:
        return start_keyboard_sounds(soundpack_dir, volume)


def is_keyboard_sounds_active() -> bool:
    """Check if keyboard sounds are currently active."""
    global _global_player
    return _global_player is not None and _global_player.is_running()
