from openai import OpenAI
import yaml
import os

models = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]


def get_openai_client():
    """Initialize and return OpenAI client with API key from config"""
    config_path = os.path.expanduser("config.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


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
