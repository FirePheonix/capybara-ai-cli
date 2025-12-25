# Keyboard Sounds Directory

This directory contains sound files for mechanical keyboard sound effects.

## 🎹 Available Soundpacks

You have 10 professional soundpacks installed in the `Soundpacks/` folder:

- **Cherry MX Black** (ABS & PBT keycaps)
- **Cherry MX Blue** (ABS & PBT keycaps) 
- **Cherry MX Brown** (ABS & PBT keycaps)
- **Cherry MX Red** (ABS & PBT keycaps)
- **NK Cream** (custom by Ryan)
- **Topre Purple Hybrid** (PBT keycaps)

## 🚀 Quick Start

1. **List all soundpacks**:
   ```
   !soundpacks
   ```

2. **Select a soundpack**:
   ```
   !select 1
   !select cherry
   !select nk-cream
   ```

3. **Toggle keyboard sounds on/off**:
   ```
   !sounds
   ```

## 📁 Directory Structure

```
sounds/
  ├── README.md (this file)
  └── Soundpacks/
      ├── cherrymx-blue-abs/      # 110+ sounds
      ├── cherrymx-blue-pbt/
      ├── cherrymx-black-abs/
      ├── cherrymx-black-pbt/
      ├── cherrymx-brown-abs/
      ├── cherrymx-brown-pbt/
      ├── cherrymx-red-abs/
      ├── cherrymx-red-pbt/
      ├── nk-cream/               # Individual key sounds
      └── topre-purple-hybrid-pbt/
```

## 🎵 Adding Custom Soundpacks

1. Create a folder in `sounds/` or `sounds/Soundpacks/`
2. Add your sound files (`.wav`, `.mp3`, or `.ogg`)
3. (Optional) Create a `config.json` for keycode mapping:

```json
{
  "id": "my-custom-pack",
  "name": "My Custom Keyboard",
  "key_define_type": "multiple",
  "defines": {
    "30": "a.wav",
    "31": "s.wav",
    "32": "d.wav"
  }
}
```

## 🔗 Download More Soundpacks

- **Rustyvibes**: https://drive.google.com/file/d/1LQEQ9aOVQAs_wgVecXkjaA9K4LXnCdp_/view?usp=sharing
- **Mechvibes**: https://docs.google.com/spreadsheets/d/1PimUN_Qn3CWqfn-93YdVW8OWy8nzpz3w3me41S8S494/edit#gid=0

## 🎛️ Features

✅ **Keycode mapping** - Each key can have its own sound
✅ **Multiple soundpacks** - Switch between different keyboard types
✅ **Random selection** - If no config.json, randomly plays sounds
✅ **32 audio channels** - Supports rapid typing without audio clipping

## 💡 Tips

- **Performance**: Lower sound file count = better performance
- **Quality**: Use OGG format for smaller file sizes
- **Volume**: Adjust in CLI with volume parameter (default: 0.3)
- **Testing**: Toggle sounds off when doing important work!

Enjoy your mechanical keyboard vibes! 🎹✨
