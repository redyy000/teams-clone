from src.data_store import data_store
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError, AccessError


def channel_invite_v1(auth_user_id, channel_id, u_id):
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


def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


def channel_join_v1(auth_user_id, channel_id):

    return {
    }

