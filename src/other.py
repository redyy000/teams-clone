import json
import jwt
from src.data_store import data_store, initial_object
from datetime import timezone
import datetime

SECRET = "RICHARDRYANDANIELMAXTAYLA"


BASE_URL = "http://127.0.0.1:{config.port}"


dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
time_stamp = int(utc_time.timestamp())


def clear_v1():
    data = data_store.get()
    data['users'].clear()
    data['channels'].clear()
    data['dms'].clear()
    data['message_ids'] = [{
        # Unique universal message id
        'message_id': 0,
        # Message type: 1 for channels, 2 for dms
        'message_type': 1,
        # Channel id or dm id
        'source_id': 0
    }]

    data['workplace_stats'] = {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_stamp}],
        'utilization_rate': 0,
    }

    data_store.set(data)


def token_create(u_id, session_id):
    '''
    Given a u_id and a session_id, generate a unique token

    Arguments:
        u_id (int)          - Unique user id
        session_id (int)    - Current session id

    Exceptions:

    Return Value:
        token (json)        - Token from unique user id and current session id
    '''
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
    data = data_store.get()

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
