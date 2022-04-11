from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.other import is_valid_token
from datetime import timezone
import datetime


def create_time_stamp():
    '''
    Return the current UTC time_stamp
    '''
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp


def channels_list_v2(token):
    '''
    Provide a list of all channels (and their associated details) that the authorised user is part of.

    Arguments:
        token (string)  - an authorisation hash of the user

    Exceptions:
        AccessError     - Occurs when token is invalid.

    Return Value:
        'channels'      - A list of dictionaries containing channel ID's and names for each channel they are a part of 

    '''
    store = data_store.get()

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(
            description=f"User ID {token} is invalid. Unable to access any details with this ID.")

    auth_user_id = token_decoded["u_id"]

    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        # If user is in the channel
        for member in channel['all_members']:
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


def channels_listall_v2(token):
    '''
    Provide a list of all channels, including private channels, (and their associated details)

    Arguments:
        token           - A JWT.

    Exceptions:
        AccessError     - Occurs when auth_user_id is invalid.

    Return Value:
        'channels'      - A list of dictionaries containing channel ID's and names for each channel that exists 

    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    store = data_store.get()
    channel_details = []
    # For each channel in the list of channels
    for channel in store['channels']:
        channel_info = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channel_details.append(channel_info)
    return {
        'channels': channel_details
    }


def channels_create_v2(token, name, is_public):
    '''
    Function to create a named channel either private or public
    Arguments:
        token (string) - an authorisation hash of the user
        name (string)         - channel name
        is_public (boolean)   - True if the channel is public, False if it's private
    Exceptions:
        AccessError  -  Occurs when token is invalid.
        InputError   -  Occurs when no channel name entered or name is greater than 20 characters.
        InputError   -  Occurs when duplicate channel name is entered. 
        InputError   -  Occurs when public status return is invalid. 
    Return Value:
        a dictionary {channel_id}

    '''
    # Check token is valid
    data = data_store.get()

    #  Check for valid user ID i.e. token
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description="Invalid Token")

    auth_user_id = token_decoded["u_id"]

    channel_id = int(len(data['channels']) + 1)

    new_channel = {'channel_id': channel_id,
                   'name': name,
                   'owner_members': [auth_user_id],
                   'all_members': [
                       {'user_id': auth_user_id,  # add the owner to the members list
                        'permission_id': 1}  # owner has permission_id = 1
                   ],
                   'is_public': is_public,
                   'messages': []
                   }

    # Check for valid channel name, between 1 and 20 characters
    if len(name) == 0 or len(name) > 20:
        raise InputError(
            description="No channel name is entered or channel name is longer than 20 characters.")

    # Check for duplicate channel names
    for channel in data['channels']:
        if channel['name'] == new_channel['name']:
            raise InputError(
                description="This channel name already exists, please create a new channel name or request to join this channel.")

    # Check is_public returns boolean
    if type(is_public) != bool:
        raise InputError(
            description="Something went wrong, unable to determine if channel is public or private.")

    # Append the new channel to the list of channels
    data['channels'].append(new_channel)

    # Update stats
    # Increase amount of channels for seams stats
    time_stamp = create_time_stamp()
    seams_channel_entry = {
        'num_channels_exist': data['workspace_stats']['channels_exist'][-1]['num_channels_exist'] + 1,
        'time_stamp': time_stamp
    }
    data['workspace_stats']['channels_exist'].append(seams_channel_entry)

    # Increase amount of channels joined for each member of channel.
    # Increase channels_joined stat for each one....
    # Suspicious usage of u_id to find user index
    user_channel_entry = {
        'num_channels_joined': data['users'][auth_user_id - 1]['stats']['channels_joined'][-1]['num_channels_joined'] + 1,
        'time_stamp': time_stamp
    }
    data['users'][auth_user_id -
                  1]['stats']['channels_joined'].append(user_channel_entry)

    data_store.set(data)

    return {
        'channel_id': channel_id
    }
