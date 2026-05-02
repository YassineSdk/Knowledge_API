from ..utils.logger_setup import logger
import numpy as np 
from rank_bm25 import BM25Okapi


def rank_documents(model,q_documents,q_reform):
    """
    this function works as a ranking engine that uses a hybrid approach where it combines 
    embeddings and BM25 ranking and information retrievel techniques in order to Keep the relevant documents to the query 

    """
    Documents = [
        (
        (r.get('title') or ' ') + 
        (r.get('content') or ' ') +
        (r.get('raw_content') or ' ')
        ) for r in search_results
    ]

    # --BM25 
    tokenized = [doc.lower().split() for doc in Documents]
    bm25 = BM25Okapi(tokenized)
    bm25_scores = bm25.get_scores(q_reform.lower().split())
    bm25_ranks = np.argsort(bm25_scores)[::-1]

    # --embedding 
    Document_emb = model_emb.encode(Documents,normalize_embeddings=True)
    query_emb = model_emb.encode(q_reform,normalize_embeddings=True)
    emb_scores = np.dot(Document_emb,query_emb.T)
    emb_ranks = np.argsort(emb_scores)[::-1]

    #--RRF Reciprocal Ranking Fusion 
    k = 60 
    RRf_scores = {}

    # BM_scores :
    for rank , idx in enumerate(bm25_ranks):
        RRf_scores[idx] = RRf_scores.get(idx, 0) + 1/(k + rank)
    
    # Emb_scores :
    for rank , idx in enumerate(emb_ranks):
        RRf_scores[idx] = RRf_scores.get(idx, 0) + 1/(k + rank)

    final_rank = sorted(RRf_scores, key=RRf_scores.get, reverse=True)

    # Ranking the documents list 
    #ranked_documents = [q_documents[int(i)] for i in final_rank]
    return final_rank
    

