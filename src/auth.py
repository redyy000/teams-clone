import hashlib
import re
from src.error import InputError, AccessError
from src.other import token_create, is_valid_token
from src.data_store import data_store
SECRET = "RICHARDRYANDANIELMAXTAYLA"


def hash(string):
    '''
    Given a string, hash with the provided secret string.


    Arguments:
        string (string)    - String to be hashed

    Exceptions:
        None

    Return Value:
        hashed_string (string) - Hashed string with SHA256
    '''

    return hashlib.sha256(string.encode()).hexdigest()


def auth_login_v2(email, password):
    '''

    Given an email and a password, validate the given inputs with the server.
    Return the appropriate auth_user_id
    or throw an exception if the inputs are incorrect.

    Arguments:
        email (string)    - Email string that accepts regular expression
        password (string)    - Password for the email address
        ...

    Exceptions:
        InputError  - Occurs when password for a given email address is incorrect
        InputError  - Occurs when a given email does not exist

    Return Value:
        {
            'token'   : token_create(user['auth_user_id'], max(user['session_id']) + 1),
            'auth_user_id' : user['auth_user_id']
        }
    '''

    store = data_store.get()

    # Hash inputted password with correct secret and encryption code

    for user in store['users']:
        if user['email'] == email:
            if user['password'] != hash(password):
                raise InputError(description="Incorrect Password!")
            else:
                # Newest session id is equal to the max session id in the user's session id list + 1
                # This means that if a session id is removed,
                # then that session id number will not be reused.
                new_session_id = max(user['session_id_list']) + 1
                # Append the newest session id to the list
                user['session_id_list'].append(new_session_id)
                data_store.set(store)
                return {
                    'token': token_create(user['u_id'], new_session_id),
                    'auth_user_id': user['u_id']
                }
    raise InputError(description="Email does not exist!")


def create_handle_str(store, name_first, name_last):
    '''

    Given a name_first and name_last, create a new handle_str and return it
    All handle_str made are unique to its user, and automatically changed
    If a given handle_str already exists in the Datastore.

    Arguments:
        store (Datastore)    - Data of all saved users
        name_first (string) - String containing first name, between 1-50 characters inclusive.
        name_last (string) - String containing last name, between 1-50 characters inclusive.


    Exceptions:
        None

    Return Value:
        Returns newly created handle_str

    '''
    # Create handle_str
    concat_str = name_first.lower() + name_last.lower()
    handle_str = ''.join(char for char in concat_str if char.isalnum())
    if len(handle_str) > 20:
        handle_str = handle_str[0:20]

    # Check for duplicate handles...
    # Modify handle_str if duplicate exists.
    is_duplicate = True
    temp_handle_str = handle_str
    counter = 0
    while is_duplicate is True:
        for user in store['users']:
            if user['handle_str'] == temp_handle_str:
                temp_handle_str = handle_str + str(counter)
                counter += 1
                break
        else:
            is_duplicate = False

    if temp_handle_str != handle_str:
        handle_str = temp_handle_str

    return handle_str


def auth_register_v2(email, password, name_first, name_last):
    '''
    Given an email, password, name_first and name_last, create a new handle_str and auth_user_id
    Proceed to save this new user as a dictionary containing the given inputs as well as handle_str and auth_user_id
    Dictionary will enter the DataStore class as part of the dictionary key 'users' list.


    ARGUMENTS:
        email (string)    - Email string that accepts regular expression
        password (string)    - Password for the email address, 6 or more characters long.
        name_first (string) - String containing first name, between 1-50 characters inclusive.
        name_last (string) - String containing last name, between 1-50 characters inclusive.
    ...

    EXCEPTIONS:
        InputError  - Occurs when name_first string is not between 1-50 characters inclusive.
        InputError  - Occurs when name_last string is not between 1-50 characters inclusive.
        InputError  - Occurs when email string is not a valid regular expression.
        InputError  - Occurs when email string matches an already existing entry.
        InputError  - Occurs when password is not 6 or more characters long.


    RETURN:
        Returns auth_user_id and token on successful creation of a new user entry.


    '''
    store = data_store.get()

    # Determine if email matches regular expression.
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if (re.fullmatch(regex, email)) == None:
        raise InputError(
            description="Email does not match the regular expression!")

    # Determine if email already exists in users list.
    for user in store['users']:
        if user['email'] == email:
            raise InputError(description="Email already exists within system!")

    # Determine if password length is 6 or more letters long

    if len(password) < 6:
        raise InputError(description="Password is too short!")

    # Determine if name_first and name_last are appropriate lengths (1-50 char)
    # This will test name_first initially; if both first name and last name
    # Are incorrect, then only the first name error will be raised.
    if len(name_first) > 50 or len(name_first) <= 0:
        raise InputError(description="First name length is invalid!")

    if len(name_last) > 50 or len(name_last) <= 0:
        raise InputError(description="Last name length is invalid!")

    # Create auth_user_id
    auth_user_id = len(store['users']) + 1

    # Create a seams permission id
    # 1 == Global Owner, automatically assigned to the first registered user
    # 2 == Normal member
    permission_id = 2
    if len(store['users']) == 0:
        permission_id = 1

    # Create user dictionary
    user = {
        'u_id': auth_user_id,
        'email': email,
        'password': hash(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': create_handle_str(store, name_first, name_last),
        'session_id_list': [1],
        'permission_id': permission_id,
        'is_deleted': False,
        'notifications': []
    }

    store['users'].append(user)
    data_store.set(store)

    return {
        'auth_user_id': auth_user_id,
        'token': token_create(user['u_id'], user['session_id_list'][0])
    }


def auth_logout_v1(token):
    '''
    Given a token, invalidate the token.


    ARGUMENTS:
        Token (jwt)
    ...

    EXCEPTIONS:
        InputError - No token is given.
        AccessError - Given token is an invalid token

    RETURN:
        {}
    '''

    # Remove the session from the session list

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    data = is_valid_token(token)
    datastore = data_store.get()

    for user in datastore['users']:
        if user['u_id'] == data['u_id']:
            user['session_id_list'].remove(data['session_id'])
    data_store.set(datastore)

    return {}
