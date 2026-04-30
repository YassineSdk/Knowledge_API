from ..utils.cleaning_text import clean_raw_text
import json
from tqdm import tqdm
from pathlib import Path 
from ..utils.logger_setup import logger
from datetime import datetime as dt

def clean_documents(store_documents:dict):
    """
    takes each websearch query documents (results) and clean the text content 
    """
    logger.info('task_3 : Documents cleaning started',
                date= dt.today().isoformat())

    if not isinstance(store_documents,dict):
        logger.error("The store documents is not a dict")
        raise ValueError("The store documents is not a dict")
    
    for q, documents in tqdm(store_documents.items(), desc = "Cleaning Documents text ...",unit="query"):
        tqdm.write(f"Cleaning Documents of Query : {q}")
        logger.info(f"Cleaning Documents for query {q}", query=q)

        if not isinstance(documents,list):
            logger.error("the document must be a list")
            raise ValueError("the document must be a list")
    
        for doc in documents:
            doc['content'] = clean_raw_text(doc.get('content', ""))
            doc['raw_content'] = clean_raw_text(doc.get('raw_content', ""))

    
    # storing the clean documents in a json file 
    dest_path = Path("dev_API/files/clean_docs.json")
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Saving cleaned documents", path=str(dest_path))
    with open(dest_path,"w",encoding="utf-8") as f:
        json.dump(store_documents, f, ensure_ascii=False, indent=4)
    
    logger.info("Document cleaning completed")
    
    return store_documents
