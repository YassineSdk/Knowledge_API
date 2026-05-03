import json 
import time 
from pathlib import Path 

CACHE_DIR = Path("dev_API/cache")
CACHE_TTL = 60 * 60 



def get_cache_path(mission_id:str)-> Path:
    return CACHE_DIR / f"chunks_{mission_id}.json"


def save_cache(mission_id:str,chunks:dict[str,list])-> None:
    CACHE_DIR.mkdir(parents=True,exist_ok=True)
    payload = {
        "timestamp":time.time(),
        "chunks":chunks
    }

    with open(get_cache_path(mission_id),"w",encoding="utf-8") as f :
        json.dump(payload, f)


def load_cache(mission_id:str)-> dict | None :
    path = get_cache_path(mission_id)

    if not path.exists():
        raise FileNotFoundError(f"the chunks files for session {mission_id} is not found")
    
    with open(path,"r",encoding="utf-8") as f :
        payload = json.load(f)
    
    if time.time() - payload['timestamp'] > CACHE_TTL:
        path.unlink() # deletes the expired file 
        return None 
    
    return payload["chunks"]



def clear_cache(mission_id: str) -> None:
    path = get_cache_path(mission_id)
    if path.exists():
        path.unlink()

