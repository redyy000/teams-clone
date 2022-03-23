import datetime
from src.error import InputError, AccessError
from src.other import load_data, store_data, SECRET, is_valid_token


def dm_create_v1():
    pass


def dm_remove_v1():
    pass


def dm_details_v1():
    pass


def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id. 
    Note: Each message should have it's own unique ID, 
    i.e. no messages should share an ID with another message, 
    even if that other message is in a different channel or DM.
    '''

    store = load_data()
    sender_id = payload['user_id']
    dm_data = store['dm_data_structure']
    payload = is_valid_token(token, SECRET)

    if payload is False:
        raise AccessError(description="Invalid token")

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

    message_id = store['message_ids'][-1]['message_id'] + 1
    store_messages = {
        'message_id': message_id,
        'message_type': 2,
        'source_id': dm_id
    }
    store['message_ids'].append(store_messages)

    new_message = {
        'message_id': message_id,
        'sender_id': sender_id,
        'message': message,
        'time_sent': datetime.datetime.now()
    }

    for dms in dm_data:
        if dms['dm_id'] == dm_id:
            dms['messages'].append(new_message)

    store_data(store)

    return message_id


def dm_list_v1():
    pass


'''
dm_data_structure = [ {
    # Name of dm automatically generated
    'name' : 'string',

    # dm id
    'dm_id' : number

    # List of normal member u_ids
    # Normal members == NOT owners
    'normal_members' : [],


    # List of owner u_ids
    # Original creator is first
    'owners' : [],
    
    # List of all member ids
    'all_members' : []

    # List of message dictionaries
    'messages' : [
        {

            # Message id is now the global message id
            'message_id' : int,

            # U_id of the sender
            'sender_id' : int(u_id),

            # Actual string of message
            'message' : 'string',

            # Time sent
            'time_sent' : datetime.datetime.now()
        }
    ]
'''
