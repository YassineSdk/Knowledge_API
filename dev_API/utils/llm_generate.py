from groq import Groq
from dotenv import load_dotenv, find_dotenv
import os 
from .logger_setup import logger

load_dotenv(find_dotenv())
key = os.getenv("Grok")
def llm_request(prompt:dict)-> dict:
    """
    this function is responsable for taking the system prompts and pass it to a LLM and returning a response
    arguments :
        - prompt : system prompt what the model need to perform 
        - key : model api key 

    """
    try :
        client = Groq(api_key=key)
        model = "meta-llama/llama-4-scout-17b-16e-instruct" 
        response = client.chat.completions.create(
        model=model,
        messages = [
            {"role":"system", "content":prompt["system"]},
            {"role":"user", "content":prompt["prompt"]},
        ],
        temperature=.4,
        )
        return response.choices[0].message.content.strip()
        
    except AuthenticationError:
        logger.error("Invalid Groq API key.")
        raise RuntimeError("Invalid Groq API key.")

    except RateLimitError:
        logger.error("Groq rate limit hit, slow down requests.")
        
        raise RuntimeError("Groq rate limit hit, slow down requests.")
    except BadRequestError as e:
        raise RuntimeError(f"Bad request to Groq: {e}")
    except GroqError as e:
        raise RuntimeError(f"Groq API error: {e}")
    

