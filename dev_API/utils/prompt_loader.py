import yaml
import os 

def load_prompt(prompt_name:str):
    """
    Loads a prompt YAML file from the prompt/ folder by name.
    Args:
        prompt_name (str): The filename without .yaml extension.
        e.g. "query_expansion_v1"
    Returns:
        dict: The prompt content with keys: key, desc, system, prompt.
    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(base_dir,"prompt",f"{prompt_name}.yaml")

    return base_dir , prompt_path
    
load_prompt()
