from groq import groq
import os 
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
groq_key = os.getenv("Grok")

def query_expansion(mission_topic,key,prompt_key)->list[str]:
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
    