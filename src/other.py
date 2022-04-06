import json
import jwt
from src.data_store import data_store, initial_object
from src.error import InputError, AccessError

SECRET = "RICHARDRYANDANIELMAXTAYLA"


BASE_URL = "http://127.0.0.1:{config.port}"


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


def search_v1(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels/DMs that the user has joined that match the query
    Arguments:
        token (string)      - an authorisation hash of the user conducting the search
        query_str (string)  - case insensitive search query
    Exceptions:
        InputError  - query string is more than 1000 characters
        AccessError - token is invalid
    Return Value:
        Returns {messages}
    '''
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Token not authorised to search.')

    if len(query_str) > 1000:
        raise InputError(
            description='Query string too long, 1000 characters or under only.')

    if len(query_str) < 1:
        raise InputError(description='Query string empty.')

    message_list = []

    store = data_store.get()  # check this is how we are still retrieving data

    for channel in store['channels']:
        is_in_channel = False
        for member in channel['all_members']:
            if member['u_id'] == decoded_token['u_id']:
                is_in_channel = True
                break
        if is_in_channel:
            for channel_message in channel['messages']:
                if query_str in channel_message['message']:
                    message_list.append(channel_message)

    for dm in store['dms']:
        is_in_dm = False
        if decoded_token['u_id'] in dm['members']:
            is_in_dm = True
        if is_in_dm:
            for dm_message in dm['messages']:
                if query_str in dm_message['message']:
                    message_list.append(dm_message)

    return {
        'messages': message_list
    }
