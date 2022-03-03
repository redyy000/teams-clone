from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

'''
Provide a list of all channels (and their associated details) that the authorised user is part of.

Arguments:
    auth_user_id (integer)  - an authorisation hash of the user

Exceptions:
    AccessError     - Occurs when auth_user_id is invalid.

Return Value:
    'channels'      - A list of dictionaries containing channel ID's and names for each channel they are a part of 

'''
def channels_list_v1(auth_user_id):
    if isinstance(auth_user_id, int) != True:
        raise AccessError("User ID is invalid. Unable to obtain channels list with this ID.")
    elif auth_user_id < 1:
        raise AccessError("User ID is invalid. Unable to obtain channels list with this ID.")
    store = data_store.get()
    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        # If user is in the channel
        if auth_user_id in channels['users']:
            channel_info = {
                'channel_id': channels['id'],
                'name': channels['name']
            }
            channel_details.append(channel_info)
    data_store.set(store)
    return {
        'channels': channel_details
    }
'''
Provide a list of all channels, including private channels, (and their associated details)

Arguments:
    auth_user_id (integer)  - an authorisation hash of the user

Exceptions:
    AccessError     - Occurs when auth_user_id is invalid.

Return Value:
    'channels'      - A list of dictionaries containing channel ID's and names for each channel that exists 

'''
def channels_listall_v1(auth_user_id):
    store = data_store.get()
    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        channel_info = {
            'channel_id': channels['id'],
            'name': channels['name']
        }
        channel_details.append(channel_info)
    data_store.set(store)
    return {
        'channels': channel_details
    }


def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
