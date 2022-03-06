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
    store = data_store.get()
    if isinstance(auth_user_id, int) != True or auth_user_id <= 0 or auth_user_id > len(store['users']):
        raise AccessError(f"User ID {auth_user_id} is invalid. Unable to access any details with this ID.")
    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        # If user is in the channel
        for member in channel['members']:
            if auth_user_id == member['user_id']:
                channel_info = {
                    'channel_id': channel['channel_id'],
                    'name': channel['name']
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
    if isinstance(auth_user_id, int) != True or auth_user_id <= 0 or auth_user_id > len(store['users']):
        raise AccessError(f"User ID {auth_user_id} is invalid. Unable to access any details with this ID.")
    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        channel_info = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channel_details.append(channel_info)
        data_store.set(store)
    return {
        'channels': channel_details
    }


def channels_create_v1(auth_user_id, name, is_public):
    '''
    Function to create a named channel either private or public
    Arguments:
        auth_user_id (integer)- an authorisation hash of the user
        name (string)         - channel name
        is_public (boolean)   - True if the channel is public, False if it's private
    Exceptions:
        AccessError  -  Occurs when auth_user_id is invalid.
        InputError   -  Occurs when no channel name entered or name is greater than 20 characters.
        InputError   -  Occurs when duplicate channel name is entered. 
        InputError   -  Occurs when public status return is invalid. 
    Return Value:
        a dictionary {channel_id}
    '''
    store = data_store.get()

    channel_id = len(store['channels']) + 1

    new_channel = {'channel_id': channel_id,
                   'name': name,
                   'owners': [auth_user_id],
                   'members': [
                       {'user_id': auth_user_id,  # add the owner to the members list
                        'permission_id': 1}  # owner has permission_id = 1
                   ],
                   'is_public': is_public,      
                   'messages': []       
                }
    
    #  Check for valid user ID
    if isinstance(auth_user_id, int) != True or auth_user_id < 1 or auth_user_id > len(store['users']):
        raise AccessError(f"User ID {auth_user_id} is invalid. Unable to create channel with this ID.")
    
    #Check for valid channel name, between 1 and 20 characters
    if len(name) == 0 or len(name) > 20:
        raise InputError("No channel name is entered or channel name is longer than 20 characters.")
    
    #Check for duplicate channel names
    for channel in store['channels']:
        if channel['name'] == new_channel['name']:
            raise InputError("This channel name already exists, please create a new channel name or request to join this channel.")

    #Check is_public returns boolean
    if type(is_public) != bool:
        raise InputError("Something went wrong, unable to determine if channel is public or private.")    
    
    #Append the new channel to the list of channels
    store['channels'].append(new_channel)
    data_store.set(store)
    
    return {
        'channel_id': channel_id,
    }

