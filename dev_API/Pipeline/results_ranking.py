from .utils.documents_ranking import rank_documents
from .utils.logger_setup import logger 


def rank_results(documents_store:dict,model,queries_refom:dict):
    """
    """
    if not documents_store:
        logger.error("document store is empty")
        raise ValueError("the document is empty")

    if not isinstance(documents_store,dict):
        logger.error("the documents must be a dict")
        raise ValueError("the documents must be a dict")
    
    if not queries_refom:
        logger.error("queries store is empty")
        raise ValueError("the the queries is empty")

    if not isinstance(queries_refom,dict):
        logger.error("the queries must be a dict")
        raise ValueError("the the queries must be a dict")
    if not model :
        logger.error("the model does not exist")
        raise ValueError("the model does not exist")

    for q in documents_store.keys():
        q_documents = documents_store[q]
        q_refom = queries_refom[q]

        documents_rank = rank_documents(model,q_documents,q_refom)

        if not documents_rank:
            raise ValueError("the documents rank is empty")
        documents_store[q] = [q_documents[int(i)] for i in documents_rank]
        logger.info(f'documents for query : {q} is ranked')


