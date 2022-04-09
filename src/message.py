from datetime import timezone
import datetime
from src.error import InputError, AccessError
from src.other import is_valid_token
from src.data_store import data_store


def permission_id_given_user(auth_user_id):
    store = data_store.get()
    permission = 0
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            permission = user['permission_id']
    return permission


def user_in_channel_all_members(auth_user_id):
    store = data_store.get()

    for channel in store['channels']:
        for member_dict in channel['all_members']:
            if member_dict['user_id'] == auth_user_id:
                return True

    return False


def message_send_v1(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    Note: Each message should have it's own unique ID,
    i.e. no messages should share an ID with another message,
    even if that other message is in a different channel or DM.
    Arguments:
        Token (token), user token
        channel_id (int), id of the channel to send from
        Message, string of message

    Exceptions:
        AccessError - Invalid Token
        AccessError - channel_id is valid but user is not a member of the channel
        InputError -  channel_id is invalid
        InputError -  Length of message < 1 or > 1000 characters.


    Return Value:

        {message_id }
    '''

    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']
    channel_list = store['channels']

    channel_found = False
    user_found = False
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel_found = True

    for channel in channel_list:
        for member in channel['all_members']:
            if member['user_id'] == u_id:
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
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }

    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    data_store.set(store)

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
        Message (string), string of message

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_is is valid but user is not a member of the dm
        InputError -  dm_id is invalid
        InputError -  Length of message < 1 or > 1000 characters.


    Return Value:

        {message_id }
    '''

    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']
    dm_data = store['dms']

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
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp)
    }

    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dms['messages'].append(new_message)

    data_store.set(store)
    return {'message_id': message_id}


def message_edit_v1(token, message_id, message):
    '''
    Edit a message with message id, replacing the content's with message
    If message is empty, then delete the original message
    Used for channels and dms
    Arguments:
        Token (token), user token
        Message_id (int), id of the message
        Message (string), string of message
    Exceptions:
        AccessError - Invalid Token
        InputError -  Length of > 1000 characters.
        InputError -  Message_id is invalid; not in the channel or dm.
        AccessError - Editor is neither a member of the channel/dm, nor a channel/dm owner.
                    - NOTE that just because editor is a global owner, does not mean they can edit/delete

    Return Value:
        {}
    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    user_id = token_decoded['u_id']
    datastore = data_store.get()

    message_found = False

    if len(message) > 1000:
        raise InputError(description='Message is too long!')

    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in datastore['channels']:
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:

                user_in_channel = user_in_channel_all_members(user_id)
                if permission_id_given_user(user_id) == 1 and user_in_channel == True:
                    pass
                elif user_id not in channel['owner_members'] and user_id != message_dict['u_id']:
                    raise AccessError(
                        description='You are both not a channel owner and sender of message')
                if len(message) == 0:
                    channel['messages'].remove(message_dict)
                else:
                    message_dict['message'] = message

                message_found = True

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in datastore['dms']:
            for message_dict in dm['messages']:
                if message_dict['message_id'] == message_id:
                    if user_id not in dm['owners'] and user_id != message_dict['u_id']:
                        raise AccessError(
                            description='You are both not a channel owner and sender of message')
                    if len(message) == 0:
                        dm['messages'].remove(message_dict)
                    else:

                        message_dict['message'] = message
                    message_found = True

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    data_store.set(datastore)

    return {}


def message_remove_v1(token, message_id):
    '''
    Given a message_id, delete the message.
    Used for channels and dms
    Arguments:
        Token (token), user token
        Message_id (id), id of message to be deleted

    Exceptions:
        AccessError - Invalid Token
        InputError -  Message_id is invalid; not in the channel or dm.
        AccessError - Editor is neither a member of the channel/dm, nor a channel/dm owner.
                    - NOTE that just because editor is a global owner, does not mean they can edit/delete

    Return Value:

        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    user_id = token_decoded['u_id']
    datastore = data_store.get()

    # Naive approach; Scan all channels and dms for the message_id match
    # Break upon done

    message_found = False
    # Find message, and delete it.

    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in datastore['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:

                user_in_channel = user_in_channel_all_members(user_id)
                if permission_id_given_user(user_id) == 1 and user_in_channel == True:
                    pass
                elif user_id not in channel['owner_members'] and user_id != message['u_id']:
                    raise AccessError(
                        description='You are both not a channel owner and sender of message')

                channel['messages'].remove(message)

                # Search for message_ids and delete
                message_found = True

                channel['messages'].remove(message)
                message_found = True

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in datastore['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    if user_id not in dm['owners'] and user_id != message['u_id']:
                        raise AccessError(
                            description='You are both not a channel owner and sender of message')
                    else:
                        dm['messages'].remove(message)
                        message_found = True

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    data_store.set(datastore)

    return {}
