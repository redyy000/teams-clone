from src.data_store import data_store
import jwt


def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    data_store.set(store)


def is_valid_token(token, SECRET):
    '''
    checks if a token has been tampered with
    Arguments:
        token
    Return Value:
        Returns False if the token is invalid, returns the payload if the token is valid
    '''
    data = data_store.get()
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
