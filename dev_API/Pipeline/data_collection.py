from ..utils.web_search import search_web 
import logfire
from datetime import datetime as dt
from pathlib import Path
import logging
import json
from  tqdm import tqdm
from ..utils.logger_setup import logger

def getting_documents(queries:dict):
    """
    """

    logger.info(f"task_2 : Documents gathering | queries:{len(queries.keys())} " ,
                date=dt.today().isoformat())

    if not queries :
        logger.error("the Queries dict is empty")
        raise ValueError("the Queries dict is empty")
    
    if not isinstance(queries, dict) :
        logger.error("the Queries are not a dict")
        raise TypeError("the Queries are not a dict")
    
    documents_store = {}

    for query_id, search_query in tqdm(queries.items(), desc="Collecting Knowledge",unit="query") :
        tqdm.write(f"searching for query : {query_id}")
        logger.info(f"search for {query_id} ",query=query_id)
        documents_store[query_id] = search_web(search_query)
    
    path = Path("dev_API/files/documents.json")

    logger.info('storing the documents')
    with open(path, "w", encoding="utf-8") as f:
        json.dump(documents_store, f, ensure_ascii=False, indent=4)
    
    logger.info("task_2 : Documents gathering ended successefully" , date=dt.today().isoformat())
    


