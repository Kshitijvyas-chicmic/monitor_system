import random
import string
from datetime import datetime, timedelta

token_store ={}

def generate_verification_token(length:int = 6, expiry:int =5):
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k= length))
    expiry = datetime.utcnow() + timedelta(minutes= expiry)
    return token , expiry

def save_token(email:str, token:str, expiry:datetime):
    token_store[email]=(token ,expiry)

def verify_token(email:str, token:str)->bool:
    if email not in token_store:
        return False
    stored_token  , expiry = token_store[email]
    if datetime.utcnow() > expiry:
        del token_store[email]
        return False
    if stored_token != token:
        return False
    del token_store[email]
    return True