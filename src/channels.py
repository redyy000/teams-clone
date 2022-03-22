from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.other import load_data, store_data, is_valid_token

def channels_create_v2(token, name, is_public):
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
    # Check token is valid   
    data = load_data()    
    
    #  Check for valid user ID i.e. token
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description = "Invalid Token")   

    auth_user_id = token_decoded["u_id"]

    channel_id = len(data['channels']) + 1

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
        raise InputError(description = 
            "No channel name is entered or channel name is longer than 20 characters.")
            
    # Check for duplicate channel names
    for channel in data['channels']:
            if channel['name'] == new_channel['name']:
                raise InputError(description = 
                    "This channel name already exists, please create a new channel name or request to join this channel.")

    # Check is_public returns boolean
    if type(is_public) != bool:
        raise InputError(description = 
            "Something went wrong, unable to determine if channel is public or private.")

    # Append the new channel to the list of channels
    data['channels'].append(new_channel)
    store_data(data)

    return {
        'channel_id': channel_id,
    }
