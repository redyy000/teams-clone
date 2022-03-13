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

    is_channel_exist = False
    for channel in channel_info:
        if channel['channel_id'] == channel_id:
            is_channel_exist = True

    if is_channel_exist is False:
        raise InputError("This channel does not exist!")

    # Checks to see if auth user is in the specified channel
    is_found = False
    for channel in channel_info:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['user_id'] == auth_user_id:
                    is_found = True

    # If not found, raise access error.
    if is_found is False:
        raise AccessError("Authorised user is not a member of the channel. ")

    # Checks to see if user is already in the channel
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            for members in channels['all_members']:
                if members['user_id'] == u_id:
                    raise InputError("Invitee is already in the channel")

   # Checks to see if user id or auth user id is invalid or does not exist
    is_uidfound = False
    is_authidfound = False
    for users in user_info:
        if users['u_id'] == u_id:
            is_uidfound = True
        if users['u_id'] == auth_user_id:
            is_authidfound = True

    # invalidity check continued
    # If uid is not found or id entered isn't a positive integer, raise error
    if is_uidfound is False or isinstance(u_id, int) is not True or u_id <= 0 or u_id > len(user_info):
        raise InputError("User ID is invalid. ")

    if is_authidfound is False or isinstance(auth_user_id, int) is not True or auth_user_id <= 0 or auth_user_id > len(user_info):
        raise AccessError("Authenticating user is invalid. ")

    # If all prior checks pass, create a new dictionary and append to members list in datastore
    new_member = {'user_id': u_id, 'permission_id': 0}
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_member)

    data_store.set(store)
    return {
    }


'''
    Function: Given a channel with ID channel_id that the authorised user is a member of, provide basic details about the channel.
    Arguments:
        auth_user_id (integer)- an authorisation hash of the user.
        channel_id (integer)  - id number of channel generated at creation.
    Exceptions:
        InputError    -    Occurs when channel id is invalid.
        InputError    -    Occurs when backend detail collection is not successful
        AccessError   -    Occurs when user attempting to access details is not a memnber of the channel.
        AccessError   -    Occurs when user id is invalid

    Return Value:
        Returns {name, is_public, owner_members, all_members} on successful access to details
'''


def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    is_channelfound = False
    isPublic = False

    # Checks to see if entered channel id exists
    for channels in store['channels']:
        if channels['channel_id'] == channel_id:
            is_channelfound = True
            # return channels
            if channels['is_public'] == True:
                isPublic = True

    # Checks to see if the channel_id is valid
    if is_channelfound == False or isinstance(channel_id, int) != True or channel_id <= 0 or channel_id > len(store['channels']):
        raise InputError(f"Channel ID {channel_id} is invalid. ")

    if isinstance(auth_user_id, int) != True or auth_user_id <= 0 or auth_user_id > len(store['users']):
        raise AccessError(
            f"User ID {auth_user_id} is invalid. Unable to access any details with this ID.")

    # Given a channel ID, find the correct channel and see if user is member
    is_member = False
    for channels in store['channels']:
        if channels['channel_id'] == channel_id:
            for members in channels['all_members']:
                if auth_user_id == members['user_id']:
                    is_member = True

    if is_member == False:
        raise AccessError(
            f"User ID {auth_user_id} is not a member of {channels['name']}, channel ID {channel_id} ")

    owner_id = []
    member_id = []

    # Add users and owners to the owner_ids and member_ids empty lists we've created
    for member in channels['all_members']:
        member_id.append(member['user_id'])
        if member['permission_id'] == 1:
            owner_id.append(member['user_id'])

    owner_details = []
    member_details = []

    for user in store['users']:
        for member in channels['all_members']:
            if user['u_id'] == member['user_id']:
                user_dict = {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str']
                }

                if member['permission_id'] == 1:
                    owner_details.append(user_dict)
                    member_details.append(user_dict)
                elif member['permission_id'] == 2:
                    member_details.append(user_dict)
    data_store.set(store)

    return {
        'name': channels['name'],
        'is_public': channels['is_public'],
        'owner_members': owner_details,
        'all_members': member_details,
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
    for current_channel in channel["all_members"]:
        if auth_user_id == current_channel["user_id"]:
            is_in_channel = True
    if isinstance(auth_user_id, int) == False or is_in_channel == False:
        raise AccessError("User ID is invalid")

    # return messages
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
        'messages': message_list,
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
    is_authidfound = False
    for users in user_info:
        if users['u_id'] == auth_user_id:
            is_authidfound = True
    if auth_user_id == False or isinstance(auth_user_id, int) != True or auth_user_id <= 0 or auth_user_id > len(user_info):
        raise AccessError("Authenticating user is invalid. ")

    # Checks for if user is already in the channel.
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            for members in channels['all_members']:
                if members['user_id'] == auth_user_id:
                    raise InputError("User is already in the channel")

    is_channelfound = False
    is_public = False
    # Checks to see if entered channel id exists
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            is_channelfound = True
            # If channel is indeed found, check to see if it's private
            if channels['is_public'] == True:
                is_public = True

    # If channel is valid check
    if is_channelfound == False or isinstance(channel_id, int) != True or channel_id <= 0 or channel_id > len(channel_info):
        raise InputError("Channel ID is invalid. ")
    elif is_public == False:
        raise AccessError("User is trying to access a private server")

    # If all prior checks pass, create a new dictionary and append to members list in datastore
    new_member = {'user_id': auth_user_id, 'permission_id': 2}
    for channels in channel_info:
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_member)

    data_store.set(store)

    return {
    }
