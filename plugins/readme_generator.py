import os
import pathlib
from typing import List
from .ai_utils import generate_content


def get_directory_structure(path: str, max_depth: int = 3, current_depth: int = 0) -> str:
    """Generate a tree-like directory structure"""
    if current_depth >= max_depth:
        return ""
    
    lines = []
    try:
        items = sorted(os.listdir(path))
        for item in items:
            if item.startswith('.') or item in ['node_modules', '__pycache__', 'venv', '.git']:
                continue
            
            item_path = os.path.join(path, item)
            indent = "  " * current_depth
            
            if os.path.isdir(item_path):
                lines.append(f"{indent}{item}/")
                lines.append(get_directory_structure(item_path, max_depth, current_depth + 1))
            else:
                lines.append(f"{indent}{item}")
    except PermissionError:
        pass
    
    return '\n'.join(filter(None, lines))


def read_key_files(path: str) -> dict:
    """Read important files for context"""
    key_files = {
        'package.json': None,
        'requirements.txt': None,
        'setup.py': None,
        'Cargo.toml': None,
        'go.mod': None,
        'pom.xml': None,
        'README.md': None,
        'LICENSE': None,
    }
    
    for filename in key_files.keys():
        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Limit file size to avoid token overflow
                    key_files[filename] = content[:2000] if len(content) > 2000 else content
            except Exception:
                pass
    
    return {k: v for k, v in key_files.items() if v is not None}


def scan_source_files(path: str, extensions: List[str] = ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp']) -> str:
    """Scan and summarize source files"""
    file_list = []
    try:
        for root, dirs, files in os.walk(path):
            # Skip common ignored directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    rel_path = os.path.relpath(os.path.join(root, file), path)
                    file_list.append(rel_path)
            
            # Limit to 50 files to avoid overwhelming the context
            if len(file_list) > 50:
                break
    except Exception:
        pass
    
    return '\n'.join(file_list)


def generate_readme(path: str = '.') -> str:
    """Generate a comprehensive README for the repository"""
    
    # Gather repository information
    dir_structure = get_directory_structure(path, max_depth=3)
    key_files = read_key_files(path)
    source_files = scan_source_files(path)
    
    # Construct the prompt for OpenAI
    prompt = f"""Analyze this repository and generate a comprehensive README.md file.

DIRECTORY STRUCTURE:
{dir_structure}

SOURCE FILES:
{source_files}

KEY FILES CONTENT:
"""
    
    for filename, content in key_files.items():
        prompt += f"\n--- {filename} ---\n{content}\n"
    
    prompt += """

Generate a well-structured README.md with the following sections:
1. Project Title and Brief Description
2. Features (bullet points)
3. Installation Instructions
4. Usage Examples
5. Project Structure Overview
6. Dependencies
7. Contributing (if applicable)
8. License (based on LICENSE file if present)

Make it professional, clear, and concise. Use proper markdown formatting.
"""

    try:
        readme_content = generate_content(prompt, max_tokens=2000)
        return readme_content
    except Exception as e:
        return f"Error generating README: {str(e)}"


def handle_readme_generation(args: List[str]) -> str:
    """Handle the !readme command"""
    
    if not args:
        path = '.'
    else:
        path = ' '.join(args)
    
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist"
    
    if not os.path.isdir(path):
        return f"Error: '{path}' is not a directory"
    
    return generate_readme(path)
