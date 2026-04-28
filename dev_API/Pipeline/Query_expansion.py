
from dotenv import load_dotenv, find_dotenv
import sys
import os
from ..utils.prompt_loader import load_prompt
from ..utils.llm_generate import llm_request

def query_expansion(mission_topic,prompt_key)->list[str]:
    """
    Expands a user query into multiple related queries following a 
    structure .

    This function takes a single query and uses an LLM to generate
    multiple variations of it, improving the chances of finding
    relevant documents in the knowledge base

    Args:
        Mission_topic (str): the topic , subject of the mission ex : fraud in train station paiment gate
        key (str)  : LLM API key 
        prompt_key : a key that fetches the prompt for this task from the prompt catalog a yaml file 
    Returns:
        list[str]: A list of expanded queries including the original.

    raises :
        ValueError : if one of the args is not in the right type or None or empty
        GroqError : if the tokens are expired or internal server problem
    
    """
    prompt = load_prompt(prompt_key)

    if prompt is None :
        raise ValueError("the prompt is empty")
    
    final_prompt = prompt["prompt"].format(mission_topic=mission_topic)
    if final_prompt is None :
        raise ValueError("the final prompt is empty")

    prompt_dict = {
        "system": prompt["system"],
        "prompt": final_prompt
    }
    Query_dict = llm_request(prompt_dict)
    if Query_dict is None :
        raise ValueError("the Query dict is empty")

    return Query_dict

mission = "trespassing in the railways stations"
output = query_expansion(mission,prompt_key="prompt_expansion")
print(output)
