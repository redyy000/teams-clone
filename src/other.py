
from src.error import InputError, AccessError
from src.other import secret
import pickle
import src.server
import requests
import jwt
from flask import Flask, request
from pathlib import Path
from src.data_store import data_store
from json import dumps


APP = Flask(__name__) 
    
BASE_URL = "http://127.0.0.1:{config.port}"

def store_data(data):
    '''
    Input Types:
    data --> dicionary (may be empty)
    
    Given a set of data, overwrite data.p with new data
    '''
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(data))

@APP.route("/clear/v2", methods = ["DELETE"])
def clear_v1():
    '''
    Input Types:
    None
    
    Sets data in data.p to a default dictionary of empty lists
    '''
    DATA_STRUCTURE = {
        "users": [],
        "channels": [],
        "dms": [],
        "messages": [],
    }
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(DATA_STRUCTURE))  

def load_data():
    '''
    Input Types:
    None
    
    load_data from data.p as a readable data structure
    '''
    if Path("data.p").exists() == False:
        requests.delete(f"{BASE_URL}/clear/v2")
    with open("data.p", "rb") as FILE:
        return pickle.loads(FILE.read())

    
    
    
def token_create(u_id, session_id):
    '''
    Given a u_id and a session_id, generate a unique token

    Arguments:
        u_id (int)          - Unique user id     
        session_id (int)    - Current session id

    Exceptions:
        InputError: Any given argument is NOT an integer

    Return Value:
        token (json)        - Token from unique user id and current session id
    '''
    
    if isinstance(u_id, int) is False or isinstance (session_id, int) is False:
        raise InputError('One or more of the inputted ids are not integers!')
    
    return jwt.encode({'u_id' : u_id, 'session_id' : session_id}, secret, algorithms = ['HS256'])



def token_decode(token):
    '''
    Given a token, decode and return the token's u_id and session_id in the form of a dictionary

    Arguments: 
        token (json)        - Token from unique user id and current session id

    Exceptions:
        InputError: Decoded token's u_id and session_id do not exist in the user database

    Return Value:
        {
            'u_id' : u_id in token, 
            'session_id : session_id in token
        }
    '''
    
    # Still need to add checks for exceptions
    
    datastore = load_data()
    decoded_token = jwt.decode(token, secret, algorithms="HS256")
    
    for user in datastore['users']:
        if user == decoded_token['u_id']:
            if decoded_token['session_id'] in user['session_id_list']:
                return decoded_token
            
    raise(InputError('Token u_id/session_id not found in the user datastore'))
    
    
    # return jwt.decode(token, secret, algorithms="HS256")
    pass
    
    
    
    
    
