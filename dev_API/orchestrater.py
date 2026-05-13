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
from .Pipeline.token_evaluation import evaluation_tokens
from .Pipeline.synthese_collection import synthesis_Knowledge
from .utils.cache_manager import load_cache



def full_pipeline(mission_id,mission,emb_model,encoder_model)-> dict[str,list]:
    """
    doctstring

    """
    # #--Query expansion :
    queries = expand_queries(mission,"query_expansion")

    # #--Web search 
    # store_documents = getting_documents(mission_id,queries)
    
    # # #--Documents raw_content and content text cleaning 
    # store_documents_v1 = clean_documents(mission_id,store_documents)

    # # #--Documents chunking
    # chunks_store = chunking_documents_store(mission_id,store_documents_v1)

    # #--Queries reformation
    queries_refom = reformulate_queries(mission,queries,prompt_key="queries_reformulation")

    # #--Chunks first level Ranking 
    # chunks_store_R1 = rank_docs_chunks(mission_id,chunks_store,emb_model,queries_refom,top_k=300)

    chunks_store_R1 = load_cache(mission_id,"chunks_ranked_R1")

    # #--Reranking the chunks using the  cross_encoder
    chunks_store_R2 = cross_encoder_rerank(mission_id,chunks_store_R1,queries_refom,encoder_model)

    # Token evaluation 
    #chunks_store_R2 = load_cache("mission_1","R2")
    #tokens_report = evaluation_tokens(chunks_store_R2)

    synthesis_Knowledge(mission_id,"prompt_Synthesis",chunks_store_R1)



