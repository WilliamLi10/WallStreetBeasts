import uuid
from datetime import datetime, timedelta
from pymongo import MongoClient

TOKEN_EXPIRATION_TIME = 7200

def gen_token(username):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wsbdb']
    tokens = db['tokens']
    token = str(uuid.uuid4())
    tokens.insert_one({'username': username, 'token': token})
    return token

def verify_token(token):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wsbdb']
    tokens = db['tokens']
    token_found = tokens.find_one({'token': token})
    if token_found is not None:
        return token_found['username']
    else:
        return None
    
def delete_token(token):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wsbdb']
    tokens = db['tokens']
    tokens.delete_one({'token': token})