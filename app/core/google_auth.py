from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from app.core.config import GOOGLE_CLIENT_ID # Ensure this is in config

def verify_google_token(token: str):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return id_info
    except ValueError:
        # Invalid token
        raise HTTPException(status_code=401, detail="Invalid Google token") 


