from src.error import InputError
import pickle
import requests
import jwt
from pathlib import Path

SECRET = "RICHARDRYANDANIELMAXTAYLA"


BASE_URL = "http://127.0.0.1:{config.port}"


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
        "message_ids": [],

    }
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(DATA_STRUCTURE))


def store_data(data):
    '''
    Input Types:
    data --> dicionary (may be empty)

    Given a set of data, overwrite data.p with new data
    '''
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(data))


def load_data():
    '''
    Input Types:
    None

    load_data from data.p as a readable data structure
    '''
    if Path("data.p").exists() == False:
        requests.delete(f"{BASE_URL}/clear/v1")
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

    if isinstance(u_id, int) is False or isinstance(session_id, int) is False:
        raise InputError(
            description='One or more of the inputted ids are not integers!')

    return jwt.encode({'u_id': u_id, 'session_id': session_id}, SECRET, 'HS256')


def is_valid_token(token):
    '''
    Given a token, decode and return the token's u_id and session_id in the form of a dictionary
    Raise an InputError if the decoded token does not correspond to an authorised user

    Arguments: 
        token (json)        - Token from unique user id and current session id

    Exceptions:
        None

    Return Value:
        {
            'u_id' : u_id in token, 
            'session_id : session_id in token
        }

        OR 

        False
    '''
    data = load_data()

    try:
        payload = jwt.decode(token, SECRET, 'HS256')
    except:
        return False
    else:
        user = next(
            (user for user in data['users'] if user['u_id'] == payload['u_id']), False)
        if user:
            if user['session_id_list'].count(payload['session_id']) != 0:
                return payload
        return False
