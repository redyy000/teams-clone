from datetime import timezone
import datetime
from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import token_create, is_valid_token
from src.user import user_profile_v1
from src.data_store import data_store


def users_list_all_v1(token):
    '''
    Given a token,
    Decode and evaluate the token to find authorised user
    Return a list of all users

    Arguments:
        token (token), token for authentication

    Exceptions:
        AccessError: Invalid Token

    Return Value:
        { 'users' : [List of all users]}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError('False Token!')

    datastore = data_store.get()
    user_list = []

    for user in datastore['users']:
        if user['is_deleted'] == False:
            user_dict = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'profile_img_url': user['profile_img_url']
            }
            user_list.append(user_dict)
    return {
        'users': user_list
    }


def users_stats_v1(token):
    '''
    Given a token,
    Return workspace_stats:
    The number of channels that exist currently
    The number of DMs that exist currently
    The number of messages that exist currently
    The workspace's utilization, which is a ratio of the number of users who have joined at least one channel/DM to the current total number of users, 
    as defined by this pseudocode: num_users_who_have_joined_at_least_one_channel_or_dm / num_users

    Arguments:
        token (token), token for authentication

    Exceptions:
        AccessError: Invalid Token

    Return Value:
        { workspace_stats }
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError('False Token!')

    datastore = data_store.get()

    num_channels_exist = len(datastore['channels'])
    num_dms_exist = len(datastore['dms'])
    num_messages_exist = 0
    for channel in datastore['channels']:
        num_messages_exist = num_messages_exist + len(channel['messages'])

    for dm in datastore['dms']:
        num_messages_exist = num_messages_exist + len(dm['messages'])

    num_users = len(datastore['users'])
    num_users_joined = 0

    for user in datastore['users']:
        u_id = user['u_id']
        is_joined = False
        for channel in datastore['channels']:
            for member_dict in channel['all_members']:
                if u_id == member_dict['user_id']:
                    is_joined = True
                    break

        for dm in datastore['dms']:
            if u_id in dm['all_members']:
                is_joined = True
                break

        if is_joined == True:
            num_users_joined = num_users_joined + 1

    utilization = float(num_users_joined)/float(num_users)
    '''
    Dictionary of shape {
     channels_exist: [{num_channels_exist, time_stamp}], 
     dms_exist: [{num_dms_exist, time_stamp}], 
     messages_exist: [{num_messages_exist, time_stamp}], 
     utilization_rate 
    }
    '''

    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    time_stamp = int(utc_time.timestamp())

    stats = {
        'channels_exist': [{num_channels_exist, time_stamp}],
        'dms_exist': [{num_dms_exist, time_stamp}],
        'messages_exist': [{num_messages_exist, time_stamp}],
        'utilization_rate': utilization


    }
    return {
        'workplace_stats': stats
    }
