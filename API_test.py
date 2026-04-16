from tavily import TavilyClient 
APIKEY = "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"

def web_search(query,max_results, KEY):
    tav_client = TavilyClient(api_key=KEY)
    response = tav_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_domains = [
    # US
    "fra.dot.gov",
    "ntsb.gov",
    "transit.dot.gov",

    # EU
    "era.europa.eu",
    "europa.eu",

    # UK
    "orr.gov.uk",
    "gov.uk",
    "raib.gov.uk",

    # Canada
    "tc.gc.ca",

    # Global
    "unece.org",
    "iso.org",
    "oecd.org",
    "worldbank.org",

    # Research
    "ieee.org",
    "sciencedirect.com",
    "springer.com"
    ],
        include_answer=True
    )
    return print(response)
    

query = "causes of cashflow loss "
web_search(query,10,APIKEY)