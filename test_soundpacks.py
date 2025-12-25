"""
Quick test script for keyboard sounds
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from plugins.soundpack_manager import discover_soundpacks, format_soundpack_list

sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
soundpacks = discover_soundpacks(sounds_dir)

print("Found soundpacks:")
for pack in soundpacks:
    print(f"  - {pack.name}: {pack.sound_count} sounds")
    print(f"    Path: {pack.path}")
    config_file = pack.path / "config.json"
    if config_file.exists():
        print(f"    Has config: YES")
    print()

print(f"\nTotal: {len(soundpacks)} soundpacks")
