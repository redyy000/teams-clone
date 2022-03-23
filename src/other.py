from src.error import InputError
import pickle
import requests
import jwt
from pathlib import Path

BASE_URL = "http://127.0.0.1:{config.port}"
SECRET = "RICHARDRYANDANIELMAXTAYLA"


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


def is_valid_token(token, SECRET):
    '''
    checks if a token has been tampered with
    Arguments:
        token
    Return Value:
        Returns False if the token is invalid, returns the payload if the token is valid
    '''
    data = load_data()
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        jwt.exceptions.InvalidSignatureError()
        return False
    else:
        user = next(
            (user for user in data['users'] if user['user_id'] == payload['user_id']), False)
        if user:
            if user['session_id_list'].count(payload['session_id']) != 0:
                return payload
        return False
