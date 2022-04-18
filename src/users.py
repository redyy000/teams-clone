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

    # Use lambda function to filter out deleted users
    valid_list = list(
        filter(lambda user: user['is_deleted'] is False, datastore['users']))

    for user in valid_list:
        user_list.append(user_profile_v1(token, user['u_id'])['user'])

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

    # Used for calculating user involvement
    # General stats of seams

    # Does this count removed users?
    # No remove the removed users...
    num_users = len([user for user in datastore['users']
                     if user['is_deleted'] == False])
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

    stats = datastore['workspace_stats']
    stats['utilization_rate'] = utilization

    return {
        'workspace_stats': stats
    }
