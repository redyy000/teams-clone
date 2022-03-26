
from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import token_create, is_valid_token, load_data, store_data
from src.user import user_profile_v1


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

    datastore = load_data()
    # user_list = [user_profile_v1(token, user['u_id'])['user']
    # for user in datastore['users'] if user['is_deleted'] == False]
    user_list = []

    for user in datastore['users']:
        if user['is_deleted'] == False:
            user_dict = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str']
            }
            user_list.append(user_dict)
    return {
        'users': user_list
    }
