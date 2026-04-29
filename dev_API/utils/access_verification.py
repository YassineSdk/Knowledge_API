
def verify_access_permission(api_key: str =Security(api_key_header)):
    if api_key != API_KEY :
        logfire.info("access denied, invalid API key")
        raise HTTPException(status_code=403, detail='invalid API Key')
    return api_key