from fastapi import FastAPI 
from pydantic import BaseModel 
import logging
import logfire 
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv("../.env")

# setup a logger 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# setup the logfire
logfire.configure(token=os.getenv("logfire_key"))



# defining the app object to create an instance of FastAPi framework 
app = FastAPI(title='Knowledge API',
            description="""this Service is responsable for generating a referencial of 
            knowledge related to a mission topic in the context of internal audit"""
            )
# autolog all the evry request, body
logfire.instrument_fastapi(app)
@app.on_event("startup")
async def on_startup():
    logger.info("=====================================")
    logger.info("Knowledge APi is starting up....")
    logger.info(f"Date : {datetime.today()}")
    logger.info("=====================================")
    logfire.info("Knowledge API started ", date=str(datetime.today()))

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("=====================================")
    logger.info("Knowledge API is shutting down....")
    logger.info("=====================================")
    logfire.info("Knowledge API closed ", date=str(datetime.today()))

# defining the shape of the request body using pydantic Basemodel
# Pydantic automaticly validates the recieved data against the schema if missing or wrong type the FastAPI retuns an error 422
class MissionTopic(BaseModel):
    mission : str 

@app.get('/')
def root():
    return {"health checks":"very healthy"}


@app.post('/Knowledge_API')
def Knowledge_collection(mission=MissionTopic):

    logging.info(f"Received mission: {mission}")
    logfire.info(f"Received mission: {mission}")
    return {"mission_topic":mission}

