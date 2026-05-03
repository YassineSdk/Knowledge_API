from fastapi import FastAPI , Security,HTTPException, status, Depends
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
from  .orchestrater import full_pipeline
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder



# getting the key fro .env
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
    logger.info("Knowledge API started", date=str(datetime.today()))
    
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
    logger.info("Knowledge API closed", date=str(datetime.today()))


# defining the app object to create an instance of FastAPi framework 
app = FastAPI(title='Knowledge API',
            description="""this Service is responsable for generating a referencial of 
            knowledge related to a mission topic in the context of internal audit""",
            lifespan=lifespan,
            dependencies=[Depends(verify_access_permission)]
            )


# autolog all , evry request, body
logger.instrument_fastapi(app)

# defining the shape of the request body using pydantic Basemodel
# Pydantic automaticely validates the recieved data against the schema if missing or wrong type the FastAPI retuns an error 422

class MissionTopic(BaseModel):
    mission : str 

@app.get('/')
def root():
    return {"health checks":"very healthy"}


@app.post('/Knowledge_API')
def Knowledge_collection(mission: MissionTopic):

    # auth passed
    logger.info("access granted")

    # # getting the mission topic
    logger.info(f"Received mission: {mission}")

    emb_model = getattr(app.state, "emb_model", None)
    encoder_model = getattr(app.state, "encod_model", None)


    if emb_model is None:
        logger.error("Embedding model not loaded")
        raise HTTPException(status_code=503, detail="Embedding Model not loaded.")

    if encoder_model is None:
        logger.error("CrossEncoder model not loaded")
        raise HTTPException(status_code=503, detail="CrossEncoder Model not loaded.")


    chunks_store_R2 = full_pipeline(mission.mission,emb_model,encoder_model)
    
    return {
        "Ranked_chunks":chunks_store_R2
    }