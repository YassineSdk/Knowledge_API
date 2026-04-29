from fastapi import FastAPI , Security,HTTPException, status
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager
from pydantic import BaseModel 
import logfire 
from dotenv import load_dotenv,find_dotenv
import os
from datetime import datetime
from pathlib import Path
import json

# importing the toolkit 
from .Pipeline.Query_expansion import query_expansion
from .Pipeline.data_collection import getting_documents 
from .Pipeline.document_cleaning import clean_documents

load_dotenv(find_dotenv())


# setup the logfire
logfire.configure(token=os.getenv("logfire_key"),
                console=logfire.ConsoleOptions(verbose=True))
# getting the key fro .env
API_KEY = os.getenv("API_key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logfire.info("Knowledge API started", date=str(datetime.today()))
    yield
    logfire.info("Knowledge API closed", date=str(datetime.today()))

# defining the app object to create an instance of FastAPi framework 
app = FastAPI(title='Knowledge API',
            description="""this Service is responsable for generating a referencial of 
            knowledge related to a mission topic in the context of internal audit""",
            lifespan=lifespan,
            )

# autolog all the evry request, body
logfire.instrument_fastapi(app)

# acess verification using authentification system API_key
def verify_access_permission(api_key: str =Security(api_key_header)):
    if api_key != API_KEY :
        logfire.info("access denied, invalid API key")
        raise HTTPException(status_code=403, detail='invalid API Key')
    return api_key


# defining the shape of the request body using pydantic Basemodel
# Pydantic automaticely validates the recieved data against the schema if missing or wrong type the FastAPI retuns an error 422
class MissionTopic(BaseModel):
    mission : str 

@app.get('/')
def root():
    return {"health checks":"very healthy"}


@app.post('/Knowledge_API')
def Knowledge_collection(mission: MissionTopic,api_key: str =Security(api_key_header)):

    # # API authentification
    # verify_access_permission(api_key)
    logfire.info("access accepted")

    # # getting the mission topic
    logfire.info(f"Received mission: {mission}")

    # # Query expansion :
    queries = query_expansion(mission.mission,"prompt_expansion")
    logfire.info("the Query expansion process is successefull")

    # # Web search 
    getting_documents(queries)
    logfire.info("the web search process is successefull")

    # Loading the Documents from json file 
    file_path= Path("dev_API/files/documents.json")
    if not file_path.exists():
        raise FileNotFoundError("the file is not found in :", file_path)

    with open(file_path,"r",encoding="utf-8") as f:
        store_documents = json.load(f)
    
    # Documents raw text cleaning 
    store_documents_v1 = clean_documents(store_documents)

    return { "clean documents:": store_documents_v1 }

