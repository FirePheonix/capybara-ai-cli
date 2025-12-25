from openai import OpenAI
from dotenv import load_dotenv
import os

models = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]


def get_openai_client():
    """Initialize and return OpenAI client with API key from .env file"""
    # Get the directory where this script is located, then go up one level to workspace root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    env_path = os.path.join(workspace_root, ".env")
    
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    
    return OpenAI(api_key=api_key)


def generate_content(prompt, model_names=models, max_tokens=1000, temperature=0.7):
    """
    Generate content using OpenAI API with fallback models
    
    Args:
        prompt: The prompt to send to OpenAI
        model_names: List of model names to try (in order)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature (0-2)
    
    Returns:
        Generated text content
    """
    last_exception = None
    client = get_openai_client()
    
    for model_name in model_names:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            last_exception = e
            continue
    
    raise RuntimeError(f"All OpenAI models failed. Last error: {last_exception}")
