import yaml
import os

def load_prompt(prompt_name: str):
    """
    Loads a prompt YAML file from the prompt/ folder by name.
    Args:
        prompt_name (str): The filename without .yaml extension.
        e.g. "prompt_expansion"
    Returns:
        dict: The prompt content with keys: key, desc, system, prompt.
    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(base_dir, "prompt", f"{prompt_name}.yaml")

    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, "r") as f:
        prompt = yaml.safe_load(f)

    return prompt
