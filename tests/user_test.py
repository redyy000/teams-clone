import pytest
import requests
from src import config


# User All Tests
# USER PROFILE DATA STRUCTURE
'''
user = {
        'u_id'  : auth_user_id,
        'email' : email,
        'name_first' : name_first,
        'name_last'  : name_last,
        'handle_str' : create_handle_str(store, name_first, name_last),
        'session_id_list' : [1]
    }
'''


@pytest.fixture
def post_test_user():
    '''
    Creates a test user and posts for use in http testing. 
    '''
    post_test_user = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'user@gmail.com',
        'password': 'password',
        'name_first': 'FirstName',
        'name_last': 'LastName',
    })
    user_data = post_test_user.json()
    return user_data


@pytest.fixture
def post_george():
    '''
    Creates test user named George Monkey, email george@gmail.com.
    '''
    post_george = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': 'monkey',
        'name_first': 'George',
        'name_last': 'Monkey',
    })
    george_data = post_george.json()
    return george_data


@pytest.fixture
def post_bob():
    '''
    Creates test user named Bob Builder, email canwefixit@gmail.com .
    '''
    post_bob = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'canwefixit@gmail.com',
        'password': 'yeswecan',
        'name_first': 'Bob',
        'name_last': 'Builder',
    })
    bob_data = post_bob.json()
    return bob_data

# USER SETEMAIL TESTS


def test_user_setemail_invalid_token(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{config.url}/clear/v1")

    response = requests.get(f"{config.url}/user/profile/setemail/v1", json={
        'token': 'invalid_token',
        'email': 'user@gmail.com',
    })
    # 400 for AccessError
    assert response.status_code == 403


def test_user_setemail_blank_email(post_test_user):
    '''
    Tests whether the proposed email is a valid email.
    '''
    requests.delete(f"{config.url}/clear/v1")

    # attempt to put a blank email
    response = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],  # finds the token of user
        'email': '',  # attempts to set email to a blank email
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_setemail_invalid_email_regex(post_test_user):
    '''
    Tests whether the email is in the correct email format, i.e. is a valid email
    '''
    requests.delete(f"{config.url}/clear/v1")

    # attempt to put an invalid email, no @
    response1 = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'invalid.com',
    })
    # 400 for InputError
    assert response1.status_code == 400


# attempt to put an invalid email, no .com
    response2 = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'invalid@gmail',
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_user_setemail_already_exists(post_george, post_bob):
    '''
    Tests for changing an email to one that is already used by another user
    '''
    requests.delete(f"{config.url}/clear/v1")
    # attempt to change email to one already in use
    # i.e. change George's email to Bob's
    response = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_george['token'],
        'email': post_bob['email'],
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_setemail_successful(post_test_user):
    '''
    Asserts a successful change of email
    '''
    requests.delete(f"{config.url}/clear/v1")
    # changes user['email']
    requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'newuseremail@gmail.com',
    })
    assert post_test_user['email'] == 'newuseremail@gmail.com'

# USER SETHANDLE TESTS


def test_user_sethandle_invalid_token():
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{config.url}/clear/v1")

    response = requests.get(f"{config.url}/user/profile/sethandle/v1", json={
        'token': 'invalid_token',
        'handle_str': 'FirstNameLastName',
    })
    # 403 for AccessError
    assert response.status_code == 403


def test_user_sethandle_short_handle(post_test_user):
    '''
    Test if handle is less than 3 characters
    '''
    requests.delete(f"{config.url}/clear/v1")
    # attempt to put a handle < 3 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'ew',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_long_handle():
    '''
    Test if handle is more than 20 characters
    '''
    requests.delete(f"{config.url}/clear/v1")
    # attempt to put a handle >20 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'onetwothreefourfivesix',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_non_alphanumeric():
    '''
    Test if handle contains non alpha-numeric characters
    '''
    requests.delete(f"{config.url}/clear/v1")
    # attempt to put a handle >20 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'one&two',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_already_exists(post_george, post_bob):
    '''
    Tests for attempting to change a handle to one that already exists
    '''
    requests.delete(f"{config.url}/clear/v1")
    # attempt to change handle to one already in use
    # i.e. change George's handle to Bob's
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_george['token'],
        'handle_str': post_bob['handle_str'],
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_successful():
    '''
    Asserts a successful change of handle
    '''
    requests.delete(f"{config.url}/clear/v1")
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'coolnewhandle',
    })
    assert post_test_user['handle_str'] == 'coolnewhandle'


# USER SETNAME TESTS

def test_user_setname_invalid_token(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{config.url}/clear/v1")
    response1 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': 'invalid_token',
        'name_first': post_test_user['name_first'],
        'name_last': post_test_user['name_last']
    })
    # 403 for AccessError
    assert response1.status_code == 403
    response2 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': 3,
        'name_first': post_test_user['name_first'],
        'name_last': post_test_user['name_last']
    })
    # 403 for AccessError
    assert response2.status_code == 403


def test_user_setname_empty(post_test_user):
    '''
    Tests if the first name and/or last name is not empty
    '''
    requests.delete(f"{config.url}/clear/v1")
    response1 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': '',
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response1.status_code == 400
    response2 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': '',
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_user_setname_long(post_test_user):
    '''
    Tests if the first and/or last name is more than 50 characters
    '''
    requests.delete(f"{config.url}/clear/v1")
    # long first name > 50
    response1 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response1.status_code == 400
    # long last name > 50
    response2 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    })
    # 400 for InputError
    assert response2.status_code == 400

    # both > 50
    response2 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_user_setname_not_string(post_test_user):
    '''
    Tests if the name entered is a string
    '''
    requests.delete(f"{config.url}/clear/v1")
    # first name not a string
    response1 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 1,
        'name_last': post_test_user['name_last'],
    })
    # 400 for InputError
    assert response1.status_code == 400
    # last name not a string
    response2 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': 1,
    })
    # 400 for InputError
    assert response2.status_code == 400
    # both not a string
    response1 = requests.get(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 1,
        'name_last': 1,
    })
    # 400 for InputError
    assert response1.status_code == 400


def test_user_setname_successful(post_test_user):
    '''
    Tests if user_profile_setname_v1
    '''
    requests.delete(f"{config.url}/clear/v1")
    # changes user's name
    requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'New_First_Name',
        'name_last': 'New_Last_Name'
    })
    assert post_test_user['name_first'] == 'New_First_Name'
    assert post_test_user['name_last'] == 'New_Last_Name'
