from ..utils.logger_setup import logger 


def documents_ranking(model,q_documents,q):
    """
    
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
    bm25_scores = bm25.get_scores(q.lower().split())
    bm25_ranks = np.argsort(bm25_scores)[::-1]

    # --embedding 
    Document_emb = model_emb.encode(Documents,normalize_embeddings=True)
    query_emb = model_emb.encode(q,normalize_embeddings=True)
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
    ranked_documents = [q_documents[int(i)] for i in final_rank]
    return ranked_documents

