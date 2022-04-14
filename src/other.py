import json
import jwt
from src.data_store import data_store, initial_object
from datetime import timezone
import datetime
import threading

from src.error import InputError, AccessError


SECRET = "RICHARDRYANDANIELMAXTAYLA"


BASE_URL = "http://127.0.0.1:{config.port}"


dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
time_stamp = int(utc_time.timestamp())



def is_channel_member(u_id, channel_id):
    datastore = data_store.get()
    for channel in datastore['channels']:
        if channel['channel_id'] == channel_id:
            for member_dict in channel['all_members']:
                if member_dict['user_id'] == u_id:
                    return True
    return False


def is_dm_member(u_id, dm_id):
    datastore = data_store.get()
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            if u_id in dm['all_members']:
                return True
    return False


def get_channel_name(channel_id):
    datastore = data_store.get()
    for channel in datastore['channels']:
        if channel['channel_id'] == channel_id:
            return channel['name']


def get_dm_name(dm_id):
    datastore = data_store.get()
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            return dm['name']


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

    data['workspace_stats'] = {
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
            if member['user_id'] == decoded_token['u_id']:
                is_in_channel = True
                break
        if is_in_channel:
            for channel_message in channel['messages']:
                if query_str in channel_message['message']:
                    message_list.append(channel_message)

    for dm in store['dms']:
        is_in_dm = False
        if decoded_token['u_id'] in dm['all_members']:
            is_in_dm = True
        if is_in_dm:
            for dm_message in dm['messages']:
                if query_str in dm_message['message']:
                    message_list.append(dm_message)

    return {
        'messages': message_list
    }


def notifications_get_v1(token):
    '''
    Return the user's most recent 20 notifications

    Arguments:
        token (string)      - an authorisation hash of the user who is adding the ownership of the user with u_id
    Exceptions:
        AccessError - token is invalid
    Return Value:
        Returns {notifications}
    '''
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Token not authorised to search.')
    data = data_store.get()
    u_id = decoded_token['u_id']

    for user in data['users']:
        if user['u_id'] == u_id:
            # Invert notifications
            # Return up to 20 most recent
            recent_notifications = user['notifications'][::-1]
            return {'notifications': recent_notifications[:20]}


# ADDED THESE 12APR 2100
def invite_notification(u_id, id, is_channel):
    datastore = data_store.get()
    for user_dict in datastore['users']:
        if user_dict['u_id'] == u_id:
            if is_channel:  # invite to a channel
                return {"channel_id": id, "dm_id": -1, "notification_message": f"{user_dict['handle_str']} added you to {get_channel_name(id)}"}
            else:  # invite to a dm
                return {"channel_id": -1, "dm_id": id, "notification_message": f"{user_dict['handle_str']} added you to {get_dm_name(id)}"}


def react_notification(u_id, id, is_channel):
    datastore = data_store.get()
    for user_dict in datastore['users']:
        if user_dict['u_id'] == u_id:
            if is_channel:  # if being sent to a channel
                notification_message = f"{user_dict['handle_str']} reacted to your message in {get_channel_name(id)}"
                return {'channel_id': id, 'dm_id': -1, 'notification_message': notification_message}
            else:  # if being sent to a dm
                notification_message = f"{user_dict['handle_str']} reacted to your message in {get_dm_name(id)}"
                return {'channel_id': -1, 'dm_id': id, 'notification_message': notification_message}


def message_notification(u_id, id, is_channel, message):
    datastore = data_store.get()
    for user_dict in datastore['users']:
        if user_dict['u_id'] == u_id:
            if is_channel:  # if being sent to a channel
                notification_message = f"{user_dict['handle_str']} tagged you in {get_channel_name(id)}: {message[:20]}"
                return {'channel_id': id, 'dm_id': -1, 'notification_message': notification_message}
            else:  # if being sent to a dm
                notification_message = f"{user_dict['handle_str']} tagged you in {get_dm_name(id)}: {message[:20]}"
                return {'channel_id': -1, 'dm_id': id, 'notification_message': notification_message}


def reset_standup(channel_id):
    #load data
    store = data_store.get()
    
    #get channel and standup
    channel = next((c for c in store["channels"] if c["channel_id"] == channel_id), None)
    if channel == None:
        return 

    standup = channel["standup"]
    
    #clear standup data
    standup["is_active"] = False
    standup["u_id"] = 0
    standup["time_finish"] = None
    standup["buffer"] = []

    #store data
    data_store.set(store)