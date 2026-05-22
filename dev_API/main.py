from fastapi import FastAPI , Security,HTTPException, status, Depends,Query
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager
from pydantic import BaseModel 
from dotenv import load_dotenv,find_dotenv
import os
from datetime import datetime
from pathlib import Path
import json

# importing the toolkit 
from  .utils.logger_setup import logger
from .utils.cache_manager import get_cache_path,load_cache
from  .orchestrater import initial_generation_pipeline, regeneration_pipeline
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder



# getting the key fro .env
load_dotenv(find_dotenv())
API_KEY = os.getenv("API_key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# acess verification using authentification system API_key
def verify_access_permission(api_key: str =Security(api_key_header)):
    logger.info("checking the user access rights")
    if api_key != API_KEY :
        logger.info("access denied, invalid API key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

# loading the embedding model in startapp


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    logger.info("Knowledge API started")
    
    # Loading the embedding model at startup
    app.state.emb_model = SentenceTransformer(
        "all-MiniLM-L6-v2",
        cache_folder="models/"
    )

    # loading the CrossEncoder model at startup
    app.state.encod_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    cache_folder="models/"
    )

    logger.info(f"embedding Model loaded successfully — embedding dim: {app.state.emb_model.get_sentence_embedding_dimension()}")
    logger.info(" encoder Model loaded successfully ")

    yield
    logger.info("Knowledge API closed")


# defining the app object to create an instance of FastAPi framework 
app = FastAPI(title='Knowledge API',
            description="""this Service is responsable for generating a referencial of 
            knowledge related to a mission topic in the context of internal audit""",
            lifespan=lifespan,
            dependencies=[Depends(verify_access_permission)]
            )



# Note: logfire instrumentation removed, using standard Python logging

# defining the shape of the request body using pydantic Basemodel
# Pydantic automaticely validates the recieved data against the schema if missing or wrong type the FastAPI retuns an error 422

class MissionTopic(BaseModel):
    mission_id :str
    mission : str 

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post('/initail_generation')
def Knowledge_collection(mission_id:str,
                        mission_topic:str):

    # auth passed
    logger.info("access granted")

    # # getting the mission topic
    logger.info(f"Received mission: mission_id :{mission_id} - mission topic :{mission_topic}")

    emb_model = getattr(app.state, "emb_model", None)
    encoder_model = getattr(app.state, "encod_model", None)


    if emb_model is None:
        logger.error("Embedding model not loaded")
        raise HTTPException(status_code=503, detail="Embedding Model not loaded.")

    if encoder_model is None:
        logger.error("CrossEncoder model not loaded")
        raise HTTPException(status_code=503, detail="CrossEncoder Model not loaded.")
    
    #checking if the mission_id and mission are not empty
    if not mission_id or not mission_topic :
        logger.error('mission id  or mission topic variable is empty')
        raise HTTPException(
            status_code=503,
            detail='mission id  or mission topic variable is empty'
        )

    knowledge_dossier = initial_generation_pipeline(mission_id,mission_topic,emb_model,encoder_model)
    
    return {
        "knowledge dossier": knowledge_dossier
    }

@app.post('/regenate_Knowledge')
def Knowledge_collection(mission_id:str,
                        mission_topic:str):

    # auth passed
    logger.info("access granted")

    # # getting the mission topic
    logger.info(f"Received mission: mission_id :{mission_id} - mission topic :{mission_topic}")
    
    logger.info("regeneration process started")
    
    emb_model = getattr(app.state, "emb_model", None)
    encoder_model = getattr(app.state, "encod_model", None)

    if emb_model is None:
        logger.error("Embedding model not loaded")
        raise HTTPException(status_code=503, detail="Embedding Model not loaded.")

    if encoder_model is None:
        logger.error("CrossEncoder model not loaded")
        raise HTTPException(status_code=503, detail="CrossEncoder Model not loaded.")
    
    #checking if the mission_id and mission are not empty
    if not mission_topic or not mission_id :
        logger.error('mission id  or mission topic variable is empty')
        raise HTTPException(
            status_code=503,
            detail='mission id  or mission topic variable is empty')
    
    # checking if chunks store for the mission_id are stored 
    chunks_path = get_cache_path(mission_id,"chunks_store")

    if not Path(chunks_path).exists():
        logger.error(f"The chunks store for mission {mission_id} does not exist in location {chunks_path}")
        raise HTTPException(
            status_code=402,
            detail = f"The chunks store for mission {mission_id} does not exist in location {chunks_path}"
            )
    logger.info("the chunks store exists")

    knowledge_dossier = regeneration_pipeline(mission_id,mission_topic,emb_model,encoder_model)
    
    return {
        "knowledge_dossier": knowledge_dossier
    } 



@app.get("/get_Knowledge_dossier")
def get_Knowledge_dossier(mission_id:str):

    K_dossier_path = get_cache_path(mission_id,"knowledge_dossier")

    if not Path(K_dossier_path).exists():
        logger.error(f"""The knowledge dossier for Mission id {mission_id} does 
            not exist run the intail generation endpoint""")
        raise HTTPException(
            status_code=402,
            detail=f"""The knowledge dossier for Mission id {mission_id} does 
            not exist run the intail generation endpoint"""
        )

    knowledge_dossier = load_cache(mission_id,"knowledge_dossier")

    return {"knowledge_dossier": knowledge_dossier}