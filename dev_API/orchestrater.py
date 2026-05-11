from pathlib import Path
import json
import time
from sentence_transformers import SentenceTransformer 
from .Pipeline.Query_expansion import expand_queries
from .Pipeline.data_collection import getting_documents 
from .Pipeline.document_cleaning import clean_documents
from .Pipeline.documents_chunking import chunking_documents_store
from .Pipeline.document_chunks_ranking import rank_docs_chunks
from .Pipeline.cross_encoder_Rerank import cross_encoder_rerank
from .Pipeline.queries_reformation import reformulate_queries
from .utils.cache_manager import load_cache, save_cache, clear_cache
from .Pipeline.token_evaluation import evaluation_tokens

def full_pipeline(mission:str,emb_model,encoder_model)-> dict[str,list]:
    """
    doctstring

    """
    # #--Query expansion :
    queries = expand_queries(mission,"query_expansion")

    # #--Web search 
    store_documents = getting_documents(queries)
    
    # #--Documents raw_content and content text cleaning 
    store_documents_v1 = clean_documents(store_documents)

    # #--Documents chunking
    chunks_store = chunking_documents_store(store_documents_v1)

    # #--Queries reformation
    queries_refom = reformulate_queries(mission,queries,prompt_key="queries_reformulation")

    # #--Chunks first level Ranking 
    chunks_store_R1 = rank_docs_chunks(chunks_store,emb_model,queries_refom,top_k=300)

    # #--saving chunks in cache file
    save_cache("mission_1","R1",chunks_store_R1)

    # #--Reranking the chunks using the  cross_encoder
    chunks_store_R2 = cross_encoder_rerank(chunks_store_R1,queries_refom,encoder_model)

    # #--saving chunks in cache file after second reranking
    save_cache("mission_1","R2",chunks_store_R2)

    # Token evaluation 
    chunks_store_R2 = load_cache("mission_1","R2")
    tokens_report = evaluation_tokens(chunks_store_R2)

    return tokens_report


