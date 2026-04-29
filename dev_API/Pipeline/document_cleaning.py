from ..utils.cleaning_text import clean_raw_text
import json
from tqdm import tqdm
from pathlib import Path 

# loading the documents as json file 
# file_path= Path("dev_API/files/documents.json")
# if not file_path.exists():
#     raise FileNotFoundError("the file is not found in :", file_path)

# with open(file_path,"r",encoding="utf-8") as f:
#     store_documents = json.load(f)
    # print('the document is loaded')

def clean_documents(store_documents:dict):
    """
    takes each websearch query documents (results) and clean the text content 
    """
    if not isinstance(store_documents,dict):
        raise ValueError("The store documents is not a dict")
    
    for q, documents in tqdm(store_documents.items(), desc = "Cleaning Documents text ..."):
        tqdm.write(f"Cleaning Documents of Query : {q}")
        if not isinstance(documents,list):
            raise ValueError("the documents are not a in a list")
    
        for doc in documents:
            doc['content'] = clean_raw_text(doc['content'])
            doc['raw_content'] = clean_raw_text(doc['raw_content'])
        print(f"cleaned : {len(documents)}")
    
    # storing the clean documents in a json file 
    dest_path = Path("dev_API/files/clean_docs.json")

    if not dest_path.exists():
        raise FileNotFoundError("the file is not found in :", dest_path)

    with open(dest_path,"w",encoding="utf-8") as f:
        json.dump(store_documents, f, ensure_ascii=False, indent=4)
    
    return store_documents
