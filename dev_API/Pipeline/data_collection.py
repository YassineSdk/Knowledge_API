from ..utils.web_search import search_web 
import logfire
#import config
from datetime import datetime as dt
import logging
import json
from  tqdm import tqdm


logging.basicConfig(level=logging.INFO)

def getting_documents(queries:dict):
    """
    """
    if queries is None :
        raise ValueError("the Queries dict is None")
    
    if not isinstance(queries, dict) :
        raise ValueError("the Queries are not a dict")
    
    #logfire.info(f"the web search started| queries:{len(queries.keys())} |start: {dt.today()} ")
    logging.info(f"the web search started| queries:{len(queries.keys())} |start: {dt.today()} ")

    
    documents_store = {}
    for query_id, search_query in tqdm(queries.items(), desc="Collecting Knowledge") :
        tqdm.write(f"searching for query : {query_id}")
        documents_store[query_id] = search_web(search_query)
        
    #logfire.info(f"the web search is successeful | end: {dt.today()} ")
    logging.info(f"the web search is successeful | end: {dt.today()} ")
    
    path = "dev_API/files/documents.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(documents_store, f, ensure_ascii=False, indent=4)
    logging.info(f"the documents are stored successefully | end: {dt.today()} ")
    
# queries = {
#         'context_and_definition': "Définition et périmètre de l'audit du processus de paie et de gestion du personnel en entreprise",
#         'causes': 'Facteurs de risque et causes profondes des erreurs dans le processus de paie et de gestion du personnel',
#         'controls': "Contrôles internes et mesures d'atténuation pour le processus de paie et de gestion du personnel",
#         'regularisation': 'Réglementations et exigences de conformité pour le processus de paie et de gestion du personnel en France',
#         'best_practices': "Bonnes pratiques et normes internationales pour l'audit du processus de paie et de gestion du personnel",
#         'benchmarking': "Indicateurs de performance clés (KPI) pour évaluer l'efficacité du processus de paie et de gestion du personnel",
#         'real_incidents': "Exemples de cas réels d'erreurs ou d'irrégularités dans le processus de paie et de gestion du personnel et leurs conséquences" 
#         }


