from datetime import timezone
import datetime
from src.error import InputError, AccessError
from src.other import is_valid_token, load_data, store_data


def message_send_v1(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel pecified by channel_id
    Note: Each message should have it's own unique ID,
    i.e. no messages should share an ID with another message,
    even if that other message is in a different channel or DM.
    Arguments:
        Token (token), user token
        channel_id (int), id of the dm to send from
        Message: Message dictionary with info

    Exceptions:
        AccessError - Invalid Token
        AccessError - channel_id is valid but user is not a member of the dm
        InputError -  channel_id is invalid
        InputError -  Length of message < 1 or > 1000 characters.


    Return Value:

        {message_id }
    '''

    store = load_data()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    sender_id = payload['u_id']
    channel_list = store['channels']

    channel_found = False
    user_found = False
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel_found = True

    for channel in channel_list:
        for member in channel['all_members']:
            if member['user_id'] == sender_id:
                user_found = True

    if channel_found == False:
        raise InputError(description="Invalid channel ID")
    if user_found == False:
        raise AccessError(description="User not in channel")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid message length")

    message_id = 0
    if len(store['message_ids']) == 0:
        message_id = 1
    else:
        message_id = store['message_ids'][-1]['message_id'] + 1

    store_messages = {
        'message_id': message_id,
        'message_type': 1,
        'source_id': channel_id
    }
    store['message_ids'].append(store_messages)

    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    new_message = {
        'message_id': message_id,
        'sender_id': sender_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }

    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    store_data(store)

    return {'message_id': message_id}


def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id.
    Note: Each message should have it's own unique ID,
    i.e. no messages should share an ID with another message,
    even if that other message is in a different channel or DM.
    Arguments:
        Token (token), user token
        Dm_id (int), id of the dm to send from
        Message: Message dictionary with info

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_is is valid but user is not a member of the dm
        InputError -  dm_id is invalid
        InputError -  Length of message < 1 or > 1000 characters.


    Return Value:

        {message_id }
    '''

    store = load_data()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    sender_id = payload['u_id']
    dm_data = store['dms']

    dm_found = False
    user_found = False
    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dm_found = True
            if sender_id in dms['all_members']:
                user_found = True

    if dm_found == False:
        raise InputError(description="Invalid DM ID")
    if user_found == False:
        raise AccessError(description="User not in dm")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid message length")

    message_id = 0
    if len(store['message_ids']) == 0:
        message_id = 1
    else:
        message_id = store['message_ids'][-1]['message_id'] + 1

    store_messages = {
        'message_id': message_id,
        'message_type': 2,
        'source_id': dm_id
    }
    store['message_ids'].append(store_messages)

    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    new_message = {
        'message_id': message_id,
        'sender_id': sender_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }

    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dms['messages'].append(new_message)

    store_data(store)

    return {'message_id': message_id}
