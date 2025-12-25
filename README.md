# 🦫 CapybaraCLI - AI-Powered Terminal with Mechanical Keyboard Sounds

An intelligent command-line interface that combines traditional shell commands with AI capabilities, featuring rich markdown rendering, smart command suggestions powered by OpenAI, and **mechanical keyboard sound effects** inspired by [rustyvibes](https://github.com/kb24x7/rustyvibes).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🤖 AI-Powered Commands
- **AI Chat**: Ask Capybara anything with `?[your question]`
- **Command Explanations**: Get instant explanations for shell commands with `!explain [command]`
- **Smart Git Helper**: Natural language Git commands with `!git [action]`
- **File Search**: Find files using natural language with `!find [query]`
- **README Generator**: Automatically generate comprehensive README files with `!readme [path]`
- **Auto-fix Suggestions**: Get AI-powered fixes for failed commands

### 🎹 Mechanical Keyboard Sounds
- **10 Professional Soundpacks** included (Cherry MX, NK Cream, Topre)
- **Per-key sound mapping** using config.json (like rustyvibes/mechvibes)
- **OGG, WAV, MP3 support** via pygame-ce
- **Toggle on/off** anytime with `!sounds`

### 💅 Rich Terminal UI
- Beautiful panels and markdown rendering
- Syntax highlighting
- Auto-suggestions from history

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-CLi.git
   cd AI-CLi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install audio dependencies** (for keyboard sounds)
   ```bash
   pip install pygame-ce pynput
   ```

4. **Configure OpenAI API Key**
   
   Create a `config.yaml` file:
   ```yaml
   openai_api_key: "your-openai-api-key-here"
   ```
   
   Or run the CLI and it will prompt you for the key on first launch.

5. **Run the CLI**
   ```bash
   python cli.py
   ```

## 📖 Commands Reference

| Command | Description |
|---------|-------------|
| `?[query]` | Ask Capybara anything (AI chat) |
| `!explain [cmd]` | Explain a shell command |
| `!git [action]` | Smart Git helper with AI suggestions |
| `!find [query]` | Natural language file search |
| `!readme [path]` | Generate README for a repository |
| `!sounds` / `!vibes` | Toggle keyboard sounds on/off |
| `!soundpacks` | List available soundpacks |
| `!select <n\|name>` | Select a soundpack by number or name |
| `!help` | Show help panel |
| `exit` / `quit` | Exit the CLI |

## 🎹 Keyboard Sounds Usage

1. **List available soundpacks:**
   ```
   !soundpacks
   ```

2. **Select a soundpack:**
   ```
   !select 1
   !select cherry-blue
   !select nk-cream
   ```

3. **Enable/disable sounds:**
   ```
   !sounds
   ```

### Included Soundpacks
- Cherry MX Black (ABS & PBT)
- Cherry MX Blue (ABS & PBT)
- Cherry MX Brown (ABS & PBT)
- Cherry MX Red (ABS & PBT)
- NK Cream
- Topre Purple Hybrid

### Adding Custom Soundpacks

Place soundpacks in `sounds/Soundpacks/` with this structure:
```
my-soundpack/
  ├── config.json
  ├── key1.ogg
  ├── key2.ogg
  └── ...
```

Download more soundpacks:
- [Rustyvibes Soundpacks](https://drive.google.com/file/d/1LQEQ9aOVQAs_wgVecXkjaA9K4LXnCdp_/view?usp=sharing)
- [Mechvibes Soundpacks](https://docs.google.com/spreadsheets/d/1PimUN_Qn3CWqfn-93YdVW8OWy8nzpz3w3me41S8S494/edit#gid=0)

## 📁 Project Structure

```
AI-CLi/
├── cli.py                 # Main CLI application
├── config.yaml            # Configuration (API keys)
├── requirements.txt       # Python dependencies
├── ascii.txt              # ASCII art for startup
├── plugins/
│   ├── __init__.py
│   ├── ai_utils.py        # AI utility functions
│   ├── file_search.py     # File search functionality
│   ├── git_helper.py      # Git helper commands
│   ├── readme_generator.py # README generation
│   ├── keyboard_sound.py  # Keyboard sound effects
│   └── soundpack_manager.py # Soundpack discovery/selection
└── sounds/
    ├── README.md
    └── Soundpacks/        # Mechanical keyboard soundpacks
        ├── cherrymx-blue-abs/
        ├── nk-cream/
        └── ...
```

## ⚙️ Requirements

```
prompt-toolkit>=3.0.0
pyyaml>=6.0.0
rich>=13.0.0
openai>=1.0.0
pynput>=1.7.6
pygame-ce>=2.5.0
```

## 🔧 Troubleshooting

### Keyboard sounds not working
1. Make sure pygame-ce and pynput are installed:
   ```bash
   pip install pygame-ce pynput
   ```
2. Restart the CLI after installation
3. Select a soundpack with `!select 1` before enabling sounds

### API Key errors
- Ensure your `config.yaml` has a valid OpenAI API key
- Check that the key has available credits

### Permission errors (macOS)
- Grant input monitoring permission in System Preferences for keyboard sounds

## 🙏 Credits

- Keyboard sound feature inspired by [rustyvibes](https://github.com/kb24x7/rustyvibes)
- Soundpacks from [Mechvibes](https://mechvibes.com/) community

## 📄 License

MIT License - feel free to use and modify!

---

Made with ❤️ and 🦫 vibes
