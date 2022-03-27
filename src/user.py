import re
from src.error import InputError, AccessError
from src.other import is_valid_token
from src.data_store import data_store


def user_profile_v1(token, u_id):
    '''
    Given a token and a u_id,
    Evaluate the u_id and decode token,
    Then return user dictionary with information:
        user_id, email, first name, last name, and handle


    Arguments:
        token (token), token for authentication
        u_id (int), u_id of user whose info is to be returned

    Exceptions:
        InputError: Given u_id does not exist
        AccessError: Invalid token

    Return Value:
        {
            'u_id'  : u_id,
            'email' : email of u_id,
            'name_first', first name of u_id,
            'name_last', last name of u_id,
            'handle_str', handle of u_id
        }
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    return_dict = {}
    for user in datastore['users']:
        if user['u_id'] == u_id:
            return_dict = {

                'user': {
                    'u_id': u_id,
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str']
                }
            }

    return return_dict


def user_profile_setname_v1(token, name_first, name_last):
    '''
    Given a token, name_first and name_last
    Decode and evaluate the token to find authorised user
    Change user's first and last names

    Arguments:
        token (token), token for authentication
        name_first (string), new first name
        name_last  (string), new last name

    Exceptions:
        InputError: name_first not between 1-50 characters inclusive
        InputError: name_last not between 1-50 characters inclusive
        AccessError: Invalid token

    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    if isinstance(name_first, str) == False or isinstance(name_last, str) == False:
        raise InputError(description="First/Last names must be strings!")

    if len(name_first) > 50 or len(name_first) <= 0:
        raise InputError(description="First name length is invalid!")
    elif len(name_last) > 50 or len(name_last) <= 0:
        raise InputError(description="Last name length is invalid!")

    for user in datastore['users']:
        if user['u_id'] == u_id:

            user['name_first'] = name_first
            user['name_last'] = name_last

    data_store.set(datastore)
    return {}


def user_profile_setemail_v1(token, email):
    '''
    Given a token and email
    Decode and evaluate the token to find authorised user
    Change user's email to email
    Handle is not changed

    Arguments:
        token (token), token for authentication
        email (string), new email for user

    Exceptions:
        InputError: Email is an invalid email(REGEX)
        InputError: Email is already being used
        AccessError: Invalid token

    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    # Determine if email matches regular expression.
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if (re.fullmatch(regex, email)) == None:
        raise InputError(
            description="Email does not match the regular expression!")

    # Check for email already existing

    for user in datastore['users']:
        if email == user['email']:
            raise InputError(
                description="Email already exists and is being used!")

    for user in datastore['users']:
        if user['u_id'] == u_id:
            user['email'] = email

    data_store.set(datastore)
    return {}


def user_profile_sethandle_v1(token, handle_str):
    '''
    Given a token and handle_str
    Decode and evaluate the token to find authorised user
    Change user's handle to handle_str

    Arguments:
        token (token), token for authentication
        handle_str (string), new handle for user

    Exceptions:
        InputError: handle_str not between 3-20 characters inclusive
        InputError: handle_str contains non-alphanumeric characters
        InputError: handle_str already being used as a handle
        AccessError: Invalid token
    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    for user in datastore['users']:
        if handle_str == user['handle_str']:
            raise InputError(
                description="Handle already exists and is being used!")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(
            description="Handle length must be between 3-20 characters inclusive!")
    elif handle_str.isalnum() == False:
        raise InputError(description="Handle must be alphanumeric!")

    for user in datastore['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str

    data_store.set(datastore)

    return {}
