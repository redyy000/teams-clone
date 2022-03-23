from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import is_valid_token, is_valid_user_id


def channel_details_v2(token, channel_id):
    store = data_store.get()
    token_data = is_valid_token(token)

    is_channelfound = False
    isPublic = False

    # Checks to see if entered channel id exists
    for channels in store['channels']:
        if channels['channel_id'] == channel_id:
            is_channelfound = True
        if channels['is_public'] == True:
            isPublic == True

    # Checks to see if the channel_id is valid
    if is_channelfound == False or isinstance(channel_id, int) != True or channel_id <= 0 or channel_id > len(store['channels']):
        raise InputError(description=f"Channel ID {channel_id} is invalid.")

    if isinstance(token, str) != True or token_data == False:
        raise AccessError(
            f"User token {token} is invalid.")

    # Check auth_user_id
    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid.Unable to access any details with this ID. ")

    is_member = False
    for channels in store['channels']:
        if channels['channel_id'] == channel_id:
            for members in channels['all_members']:
                if auth_user_id == members['token']:
                    is_member = True

    if is_member == False:
        raise AccessError(
            description=f"User ID {auth_user_id} is not a member of {channels['name']}, channel ID {channel_id} ")

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
