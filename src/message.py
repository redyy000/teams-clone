from src.error import InputError, AccessError
from src.other import is_valid_token, message_notification, is_channel_member, is_dm_member, get_channel_name, get_dm_name, react_notification
from src.data_store import data_store
from datetime import timezone
import datetime


def create_time_stamp():
    '''
    Return the current UTC time_stamp
    '''
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = int(utc_time.timestamp())
    return utc_timestamp


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
    utc_timestamp = int(utc_time.timestamp())

    # Set reacts
    default_reacts = {
        'react_id': 1,
        'u_ids': [],
        'is_this_user_reacted': False
    }

    reacts = [default_reacts]

    new_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp),
        'reacts': reacts,
        'is_pinned': False
    }

    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    # Update seams and user messages sent
    seams_message_entry = {
        'num_messages_exist': store['workspace_stats']['messages_exist'][-1]['num_messages_exist'] + 1,
        'time_stamp': utc_timestamp
    }
    store['workspace_stats']['messages_exist'].append(seams_message_entry)

    # Increase amount of user messages sent
    user_member_entry = {
        'num_messages_sent': store['users'][u_id - 1]['stats']['messages_sent'][-1]['num_messages_sent'] + 1,
        'time_stamp': utc_timestamp
    }
    store['users'][u_id -
                   1]['stats']['messages_sent'].append(user_member_entry)
    # Add message notification if tagged...
    # Some sort of tagging function.
    # Check for @handle in string
    # Only should fire once for a single tag in a message

    for user in store['users']:
        tag = '@' + user['handle_str']
        # Check if tag in message
        # Check if member in channel

        is_member = is_channel_member(user['u_id'], channel_id)
        if tag in message and is_member:
            user['notifications'].append(message_notification(
                u_id, channel_id, True, message))

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
    utc_timestamp = int(utc_time.timestamp())

    # Set reacts
    default_reacts = {
        'react_id': 1,
        'u_ids': [],
        'is_this_user_reacted': False
    }

    reacts = [default_reacts]

    new_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_sent': int(utc_timestamp),
        'reacts': reacts,
        'is_pinned': False
    }

    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dms['messages'].append(new_message)

    # Update stats

    # Update seams and user messages sent
    seams_message_entry = {
        'num_messages_exist': store['workspace_stats']['messages_exist'][-1]['num_messages_exist'] + 1,
        'time_stamp': utc_timestamp
    }
    store['workspace_stats']['messages_exist'].append(seams_message_entry)

    # Increase amount of user messages sent
    user_member_entry = {
        'num_messages_sent': store['users'][u_id - 1]['stats']['messages_sent'][-1]['num_messages_sent'] + 1,
        'time_stamp': utc_timestamp
    }
    store['users'][u_id -
                   1]['stats']['messages_sent'].append(user_member_entry)
    data_store.set(store)
    # Add notifications for tag

    for user in store['users']:
        tag = '@' + user['handle_str']
        # Check if tag in message
        # Check if member in channel
        if tag in message and is_dm_member(user['u_id'], dm_id):
            user['notifications'].append(message_notification(
                u_id, dm_id, False, message))

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

    utc_timestamp = create_time_stamp()
    # Update seams messages sent
    seams_message_entry = {
        'num_messages_exist': datastore['workspace_stats']['messages_exist'][-1]['num_messages_exist'] - 1,
        'time_stamp': utc_timestamp
    }
    datastore['workspace_stats']['messages_exist'].append(seams_message_entry)

    data_store.set(datastore)

    return {}


def message_react_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message.
    Arguments:
        Token (token), user token
        message_id (int), id of the message which is being reacted to
        react_id (int), id of the reaction

    Exceptions:
        InputError -  message_id is invalid
        InputError -  react_id is an invalid reaction
        InputError -  Message already contains a react with this react_id
        AccessError - Invalid Token

    Return Value:
        {}
    '''
    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']

    # Naive approach; Scan all channels and dms for the message_id match
    # Break upon done

    # Message_found remains false if message cannot be found, otherwise
    # message_found is changed to the message
    # User_found checks to see whether user is in the channel/dm

    message_found = False
    user_found = False
    sender_id = False
    is_channel_message = False
    channel_dm_id = -1
    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_found = message
                sender_id = message['u_id']
                is_channel_message = True
                channel_dm_id = channel['channel_id']
                for user in channel['all_members']:
                    if user['user_id'] == u_id:
                        user_found = True

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    message_found = message
                    sender_id = message['u_id']
                    channel_dm_id = dm['dm_id']
                    for user in dm['all_members']:
                        if user == u_id:
                            user_found = True

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    if user_found == False:
        raise AccessError(description="User not in channel/dm")

    # Check if react_id is a valid reaction
    if react_id != 1:
        raise InputError(description="Invalid React ID")

    if u_id in message_found['reacts'][0]['u_ids']:
        raise InputError(
            description="Message already contains your reaction with this React ID!")

    message_found['reacts'][0]['react_id'] = 1
    message_found['reacts'][0]['u_ids'].append(u_id)
    message_found['reacts'][0]['is_this_user_reacted'] = True

    # Send a reaction notification to the original message sender.
    # Doesn't actually need the original message.
    for user in store['users']:
        if user['u_id'] == sender_id:
            user['notifications'].append(react_notification(sender_id, channel_dm_id,
                                                            is_channel_message))
    data_store.set(store)

    return {}


def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message.
    Arguments:
        Token (token), user token
        message_id (int), id of the message which is being reacted to
        react_id (int), id of the reaction

    Exceptions:
        InputError -  message_id is invalid
        InputError -  react_id is an invalid reaction
        InputError -  Message does not contain a react with this react_id

    Return Value:
        {}
    '''
    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    u_id = payload['u_id']

    # Naive approach; Scan all channels and dms for the message_id match
    # Break upon done

    # Message_found remains false if message cannot be found, otherwise
    # message_found is changed to the message
    # User_found checks to see whether user is in the channel/dm

    message_found = False
    user_found = False

    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_found = message
                for user in channel['all_members']:
                    if user['user_id'] == u_id:
                        user_found = True

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    message_found = message
                    for user in dm['all_members']:
                        if user == u_id:
                            user_found = True

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    if user_found == False:
        raise AccessError(description="User not in channel/dm")

    # Check if react_id is a valid reaction
    if react_id != 1:
        raise InputError(description="Invalid React ID")

    if u_id not in message_found['reacts'][0]['u_ids']:
        raise InputError(
            description="You have not reacted to this message with this React ID!")

    message_found['reacts'][0]['react_id'] = 1
    message_found['reacts'][0]['u_ids'].remove(u_id)
    message_found['reacts'][0]['is_this_user_reacted'] = False

    data_store.set(store)

    return {}


def message_pin_v1(token, message_id):
    '''
    Given a message within a channel or DM, mark it as "pinned".
    
    Arguments:
        Token (token), user token
        Message_id (int), id of the message
    Exceptions:
        AccessError - Invalid token
        InputError -  message_id is invalid
        AccessError - User not in channel/dm
        InputError -  Message has already been pinned
        AccessError -  User does not have owner permissions in channel/DM

    Return Value:
        {}
    '''
    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")
    
    u_id = payload['u_id']

    # Naive approach; Scan all channels and dms for the message_id match
    # Break upon done

    # Message_found remains false if message cannot be found, otherwise
    # message_found is changed to the message
    # User_found checks to see whether user is in the channel/dm

    message_found = False
    user_found = False
    has_perms = True

    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_found = message
                for user in channel['all_members']:
                    if user['user_id'] == u_id:
                        user_found = True
                if u_id not in channel['owner_members'] or permission_id_given_user(u_id) != 1:
                    has_perms = False

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    message_found = message
                    for user in dm['all_members']:
                        if user == u_id:
                            user_found = True
                    if u_id not in dm['owners'] or permission_id_given_user(u_id) != 1:
                        has_perms = False

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    if user_found == False:
        raise AccessError(description="User not in channel/dm")

    if message_found['is_pinned'] == True:
        raise InputError(description="Message has already been pinned")
    
    if has_perms == False:
        raise AccessError(description=f"User ID {u_id} does not have owner permissions in this channel.")
    
    message_found['is_pinned'] = True

    data_store.set(store)

    return {}


def message_unpin_v1(token, message_id):
    '''
    Given a message within a channel or DM, remove its mark as pinned.
    
    Arguments:
        Token (token), user token
        Message_id (int), id of the message
    Exceptions:
        AccessError - Invalid token
        InputError -  message_id is invalid
        AccessError - User not in channel/dm
        InputError -  Message has not already been pinned
        InputError -  User does not have owner permissions in channel/DM

    Return Value:
        {}
    '''
    store = data_store.get()

    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")
    
    u_id = payload['u_id']

    # Naive approach; Scan all channels and dms for the message_id match
    # Break upon done

    # Message_found remains false if message cannot be found, otherwise
    # message_found is changed to the message
    # User_found checks to see whether user is in the channel/dm

    message_found = False
    user_found = False
    has_perms = True

    # Since channel stores all_members as a list of dicts
    # Large nesting due to how all_members are stored in channels
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_found = message
                for user in channel['all_members']:
                    if user['user_id'] == u_id:
                        user_found = True
                if u_id not in channel['owner_members'] or permission_id_given_user(u_id) != 1:
                    has_perms = False

    # Reloop for DMs; If found already this is skipped.
    if message_found == False:
        for dm in store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    message_found = message
                    for user in dm['all_members']:
                        if user == u_id:
                            user_found = True
                    if u_id not in dm['owners'] or permission_id_given_user(u_id) != 1:
                        has_perms = False

    if message_found == False:
        raise InputError(description="Invalid Message ID")

    if user_found == False:
        raise AccessError(description="User not in channel/dm")

    if message_found['is_pinned'] == False:
        raise InputError(description="Message has not already been pinned")
    
    if has_perms == False:
        raise AccessError(description=f"User ID {u_id} does not have owner permissions in this channel.")

    message_found['is_pinned'] = False

    data_store.set(store)

    return {}

