from src.data_store import data_store
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError, AccessError


'''
Invites a user with ID u_id to join a channel with ID channel_id. 
Once invited, the user is added to the channel immediately. 
In both public and private channels, all members are able to invite users.

Arguments:
    auth_user_id (integer) - unique identifier for the authorised user
    channel_id   (integer) - unique identifier of the channel
    u_id         (integer) - unique identifier for the invitee
Exceptions:
    InputError - Occurs when channel_id is invalid
    InputError - Occurs when u_id does not refer to a valid user
    InputError - Occurs when u_id refers to an invitee that is already in the channel
    AccessError - Occurs when the authorised user is not a member of the channel
Return Type:
    None
'''
def channel_invite_v1(auth_user_id, channel_id, u_id):

    store = data_store.get()
    channel_info = store['channels']
    user_info = store['users']

    # Checks to see if auth user is in the specified channel
    found = False
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            for members in channels['members']:
                if members['user_id'] == auth_user_id:
                    found = True

    # If not found, raise access error.
    if found == False:
        raise AccessError("Authorised user is not a member of the channel. ")

    # Checks to see if user is already in the channel
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            for members in channels['members']:
                if members['user_id'] == u_id:
                    raise InputError("Invitee is already in the channel")

   # Checks to see if user id or auth user id is invalid or does not exist
    uidfound = False
    authidfound = False
    for users in user_info:
        if users['u_id'] == u_id:
            uidfound = True
        if users['u_id'] == auth_user_id:
            authidfound = True

    # invalidity check continued
    # If uid is not found or id entered isn't a positive integer, raise error
    if uidfound == False or isinstance(u_id, int) != True or u_id < 0 or u_id > len(user_info):
        raise InputError("User ID is invalid. ")

    if auth_user_id == False or isinstance(auth_user_id, int) != True or auth_user_id < 0 or auth_user_id > len(user_info):
        raise AccessError("Authenticating user is invalid. ")

    # If all prior checks pass, create a new dictionary and append to members list in datastore
    new_member = {'user_id': u_id, 'permission_id': 0}
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            channels['members'].append(new_member)

    data_store.set(store)
    return {

    }


def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }


'''
Given a channel with a channel ID that the authorised user (auth_user_id) is
a member of, return up to 50 messages between 'start' and 'start + 50'. If
the function has return the lease recent message in the channel return -1 to
indicate there are no more messages

Arguments:
    auth_user_id (integer) - id number of authorised user
    channel_id (integer) - id number for channel
    start (integer) - integer value of starting index (e.g. 0 for messages[0])
    ...

Exceptions:
    InputError  - Occurs when channel_id does not refer to a valid channel
    InputError  - Occurs when starting index is greater than number of messages
    AccessError - Occurs when channel_id exists but the user is not a channel member

General Exceptions
    InputError - Occurs when channel_id is not an integer
    InputError - Occurs when starting index is not an integer
    AccessError - Occurs when auth_user_id is not an integer

Return Value:
    Returns dictionary containing list of messages, the starting index (start) and
    the ending index (start + 50 or -1 if least recent message returned)
'''

def channel_messages_v1(auth_user_id, channel_id, start):
    store = data_store.get()
    
    # check channel_id invalid
    channels_list = store["channels"]
    if isinstance(channel_id, int) == False or channel_id > len(channels_list) \
    or channel_id <= 0:
        raise InputError("Channel_id is not valid!")
    
    # get channel and messages list from data_store
    channel = channels_list[channel_id - 1]
    channel_messages = channel["messages"]      
    
    # check start index invalid
    if isinstance(start, int) == False or start > len(channel_messages) or start < 0:
        raise InputError("Message index is invalid!")
    
    # check user_id invalid
    is_in_channel = False 
    for current_channel in channel["members"]:
        if auth_user_id == current_channel["user_id"]:
            is_in_channel = True
    if isinstance(auth_user_id, int) == False or is_in_channel == False:
        raise AccessError("User ID is invalid")
        
    #return messages
    message_list = []
    i = 0
    for idx in channel_messages and start in start + 50:
        message_list.append(idx)
        i += 1
    if i < 50:
        end = -1
    else:
        end = start + 50
    
    return {
        'messages': [message_list],
        'start': start,
        'end': end,
    }
'''
    Given a channel_id of a channel that the authorised user can join, adds them to that channel.
    Arguments:
        auth_user_id (integer) - unique identifier for the authorised user
        channel_id   (integer) - unique identifier of the channel
    Exceptions:
        InputError - Occurs when channel_id is invalid
        InputError - Occurs when u_id refers to an invitee that is already in the channel
        AccessError - Occurs when the authorised user tries to join a private channel and is not already a member
    Return Type:
        None
'''
def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()
    channel_info = store['channels']
    user_info = store['users']

    # Additional test for is auth user id exists
    authidfound = False
    for users in user_info:
        if users['u_id'] == auth_user_id:
            authidfound = True
    if auth_user_id == False or isinstance(auth_user_id, int) != True or auth_user_id < 0 or auth_user_id > len(user_info):
        raise AccessError("Authenticating user is invalid. ")

    # Checks for if user is already in the channel.
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            for members in channels['members']:
                if members['user_id'] == auth_user_id:
                    raise InputError("User is already in the channel")

    channelfound = False
    isPublic = False
    # Checks to see if entered channel id exists
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            channelfound = True
            # If channel is indeed found, check to see if it's private
            if channels['public_status'] == "is_public":
                isPublic = True

    # If channel is valid check
    if channelfound == False or isinstance(channel_id, int) != True or channel_id < 0 or channel_id > len(channel_info):
        raise InputError("Channel ID is invalid. ")
    elif isPublic == False:
        raise AccessError("User is trying to access a private server")

    # If all prior checks pass, create a new dictionary and append to members list in datastore
    new_member = {'user_id': auth_user_id, 'permission_id': 0}
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            channels['members'].append(new_member)

    data_store.set(store)

    return {
    }


