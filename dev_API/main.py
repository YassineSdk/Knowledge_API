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
from .Pipeline.Query_expansion import query_expansion
from .Pipeline.data_collection import getting_documents 
from .Pipeline.document_cleaning import clean_documents
from sentence_transformers import SentenceTransformer


# setup the logger


# getting the key fro .env
API_KEY = os.getenv("API_key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Knowledge API started", date=str(datetime.today()))
    yield
    logger.info("Knowledge API closed", date=str(datetime.today()))

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

# defining the app object to create an instance of FastAPi framework 
app = FastAPI(title='Knowledge API',
            description="""this Service is responsable for generating a referencial of 
            knowledge related to a mission topic in the context of internal audit""",
            lifespan=lifespan,
            dependencies=[Depends(verify_access_permission)]
            )

# loading the embedding model in startapp

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    logger.info("Knowledge API started", date=str(datetime.today()))
    app.state.model = SentenceTransformer(
        "all-MiniLM-L6-v2",
        cache_folder="models/"
    )
    logger.info(f"Model loaded successfully — embedding dim: {app.state.model.get_sentence_embedding_dimension()}")
    yield
    # --- shutdown ---
    logger.info("Knowledge API closed", date=str(datetime.today()))

    
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
    logger.info("access granded")

    # # getting the mission topic
    logger.info(f"Received mission: {mission}")

    model = getattr(app.state, "model", None)

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    return {"status": "ok", "model": "all-MiniLM-L6-v2"}

    # # # Query expansion :
    # queries = query_expansion(mission.mission,"prompt_expansion")

    # # # Web search 
    # getting_documents(queries)

    # # Loading the Documents from json file 
    # file_path= Path("dev_API/files/documents.json")
    # if not file_path.exists():
    #     raise FileNotFoundError("the file is not found in ",path = str(file_path))

    # with open(file_path,"r",encoding="utf-8") as f:
    #     store_documents = json.load(f)
    
    # # Documents raw text cleaning 
    # store_documents_v1 = clean_documents(store_documents)
    

    # return { "clean documents:": store_documents_v1 }
    return {
        "mission":mission.mission
    }

