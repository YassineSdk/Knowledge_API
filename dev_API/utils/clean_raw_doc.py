import re

def clean_raw_text(text):
    """
    this function cleans the raw content of each documents from the document store
    """

    if not isinstance(text,str):
        return ''
    # remove Ui elements [content] [comments] and links (https:xxx)
    clean_text = re.sub(r'\[.*?\]|\(.*?\)','',text,flags=re.DOTALL)
    
    # removes stray ponctuation and artifacts
    clean_text = re.sub(r'(?<!\w)[!)\'"]+(?!\w)','',clean_text)

    # removing Non back space 
    clean_text =  clean_text.replace('\xa0',' ')

    #collapsing multiple spaces 
    clean_text = re.sub('[ \t]{2,}',' ',clean_text)

    # normalising multiple new lines 
    clean_text = re.sub(r'\n{3,}','\n\n',clean_text)
    
    clean_text = clean_text.replace('\\n', ' ')
    # cleanining the repeated title fragraments 
    clean_text = re.sub(r'["\']\s*\)', '', clean_text)

    # NEW: Remove TOC trailing dots and page numbers (e.g., "......22" or ". \n 42")
    clean_text = re.sub(r'\.{2,}\s*\d+', '', clean_text)

    # Removing ### and ** 
    clean_text = re.sub(r'(?<!\w)[#\*\|\-—\+]+(?!\w)','',clean_text)
    
    return clean_text.strip()