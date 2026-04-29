from ..utils.web_search import search_web 
import logfire
#import config
from datetime import datetime as dt
import logging
import json


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
    for query_id, search_query in queries.items():
        documents_store[query_id] = search_web(search_query)
        
    #logfire.info(f"the web search is successeful | end: {dt.today()} ")
    logging.info(f"the web search is successeful | end: {dt.today()} ")
    
    path = "/home/yassine/ONCF_projects/Knowledge_API/files/documents.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(documents_store, f, ensure_ascii=False, indent=4)
    
queries = {
        'context_and_definition': 'definition and scope of trespassing in train stations and its impact on passenger safety and railway operations',
        'causes': 'root causes and risk factors contributing to passengers trespassing in train stations including infrastructure design security measures and passenger behavior',
        'controls': 'internal controls and mitigation strategies to prevent passengers from trespassing in train stations such as access control surveillance and security personnel',
        'regularisation': 'laws regulations and compliance requirements related to trespassing in train stations including railway safety regulations and passenger liability',
        'best_practices': 'industry best practices and standards for preventing and managing trespassing incidents in train stations including security protocols and emergency response plans',
        'benchmarking': 'key performance indicators KPIs and performance metrics for measuring the effectiveness of trespass prevention and response in train stations',
        'real_incidents': 'real cases and incidents of passengers trespassing in train stations including audit findings and lessons learned from previous trespassing incidents'
        }
getting_documents(queries)
