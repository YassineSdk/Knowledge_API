from pathlib import Path
import json
from .Pipeline.Query_expansion import query_expansion
from .Pipeline.data_collection import getting_documents 
from .Pipeline.document_cleaning import clean_documents
from sentence_transformers import SentenceTransformer 
from .Pipeline.documents_chunking import chunking_documents_store
from .Pipeline.document_chunks_ranking import rank_docs_chunks
from .Pipeline.queries_reformation import queries_reformulate

def inital_generation(mission,model):
    """
    doctstring

    """
    # #--Query expansion :
    queries = query_expansion(mission,"query_expansion")

    # #--Web search 
    # getting_documents(queries)

    #--Loading the Documents from json file 
    file_path= Path("dev_API/files/documents.json")
    if not file_path.exists():
        raise FileNotFoundError("the file is not found in ",path = str(file_path))

    with open(file_path,"r",encoding="utf-8") as f:
        store_documents = json.load(f)
    
    #--Documents raw text cleaning 
    store_documents_v1 = clean_documents(store_documents)

    #--Documents chunking
    chunks_store = chunking_documents_store(store_documents_v1)

    #--Queries reformation
    queries_refom = queries_reformulate(mission,queries,prompt_key="queries_reformulation")

    #--Chunks first level Ranking 
    chunks_store_R1 = rank_docs_chunks(chunks_store,model,queries_refom,top_k=150)

    return chunks_store_R1


