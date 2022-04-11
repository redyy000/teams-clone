from datetime import datetime, timezone
from threading import Timer
from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import is_valid_token


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Send a message from the authorised user to the channel
    specified by channel_id automatically at a specified time in the future.
    Note: Do not consider what happens if the user's token is invalidated or a
    user leaves before the message is scheduled to be sent

    Arguments:
        Token (token), user token
        channel_id (int), id of the channel to send from
        message (string), string of message
        time_sent (datetime), time that the message should be sent from


    Exceptions:
        InputError - Channel_id does not refer to a valid channel
        InputError - Length of message is < 1 or > 1000 characters
        InputError - Time sent is a time in the past
        AccessError - Authorised user is not part of the channel they are trying to post to.

    Return Value:
        {message_id}
    '''
    store = data_store.get()
    # Validity Checks for payload
    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']
    channel_list = store['channels']

    # Validity checks for channel and user
    channel_found = False
    user_found = False
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel_found = True
            for members in channel['all_members']:
                if members['user_id'] == u_id:
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

    # Setting delay for message
    duration = time_sent - datetime.now().timestamp()
    if duration < 0:
        raise InputError(description="Invalid time for message to be sent")
    store_messages = {
        'message_id': message_id,
        'message_type': 1,
        'source_id': channel_id
    }
    store['message_ids'].append(store_messages)

    t = Timer(duration, message_timer, args=(
        channel_id, u_id, message, message_id))
    t.start()

    # Takes latest message as return as timer function
    # doesnt allow for return values
    data_store.set(store)
    return {'message_id': message_id}

# Function to execute message sending


def message_timer(channel_id, u_id, message, message_id):
    store = data_store.get()
    channel_list = store['channels']

    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    new_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    data_store.set(store)


def message_sendlater_dm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from the authorised user to the specified DM following
    a delay. If a DM is removed, you do not need to send the message.
    Do not account for if the token is invalidated after message is sent
    or the user leaves

    Arguments:
        Token(token), User token
        dm_id(int), dm identifier
        message(string), string of message
        time_sent(time), time for message to be sent

    Exceptions:
    AccessError - Authorised user is not part of the dm 
    '''

    store = data_store.get()
    # Validity checks for token
    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']
    dm_data = store['dms']

    # Validity Checks for u_id and payload
    dm_found = False
    user_found = False
    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dm_found = True
            if u_id in dms['all_members']:
                user_found = True

    if dm_found == False:
        raise InputError(description="Invalid DM ID")
    if user_found == False:
        raise AccessError(description="User not in dm")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="Invalid message length")

    duration = time_sent - datetime.now().timestamp()
    if duration < 0:
        raise InputError(description="Invalid time for message to be sent")

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

    t = Timer(duration, dm_timer, args=(dm_id, u_id, message, message_id))
    t.start()

    # Check if
    dm_exists = False
    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dm_exists = True
    data_store.set(store)

    return {'message_id': message_id}


# Wrapper that checks if dm has been removed
def recheck(function):
    def wrapper(*args, **kwargs):
        store = data_store.get()
        dm_data = store['dms']
        for dms in dm_data:
            if dms['dm_id'] == args[0]:
                data_store.set(store)
                return function(*args, **kwargs)

        message_id = args[3]
        for x in store['message_ids']:
            if x['message_id'] == message_id:
                store['message_ids'].remove(x)
        data_store.set(store)
    return wrapper


@recheck
def dm_timer(dm_id, u_id, message, message_id):

    store = data_store.get()
    dm_data = store['dms']

    # Getting the current date
    # and time
    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    new_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }

    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dms['messages'].append(new_message)

    data_store.set(store)
