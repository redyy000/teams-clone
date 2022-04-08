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
    requests.delete(f"{config.url}/clear/v1")
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

# USER PROFILE TESTS


def test_user_profile_invalid_token(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''

    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': 'invalid_token',
        'u_id': post_test_user['auth_user_id'],
    })
    # 403 for AccessError
    assert response.status_code == 403


def test_user_profile_invalid_id(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''

    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': -1
    })
    # 403 for AccessError
    assert response.status_code == 400


def test_user_profile_valid_users(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    response1 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': george_info['auth_user_id']
    })

    assert response1.status_code == 200

    response2 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': bob_info['auth_user_id']
    })

    assert response2.status_code == 200


def test_user_profile_functionality(post_test_user):

    george_info = post_george()

    response1 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': post_test_user['auth_user_id']
    })

    user_dict = response1.json()['user']
    assert response1.status_code == 200
    assert user_dict['email'] == 'user@gmail.com'
    assert user_dict['name_first'] == 'FirstName'
    assert user_dict['name_last'] == 'LastName'
    assert user_dict['handle_str'] == 'firstnamelastname'

    response2 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': george_info['token'],
        'u_id': george_info['auth_user_id']
    })

    george_dict = response2.json()['user']
    assert response2.status_code == 200
    assert george_dict['email'] == 'george@gmail.com'
    assert george_dict['name_first'] == 'George'
    assert george_dict['name_last'] == 'Monkey'
    assert george_dict['handle_str'] == 'georgemonkey'


def test_user_profile_functionality_admin_remove(post_test_user):

    george_info = post_george()

    # Remove george :(
    requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': post_test_user['token'],
        'u_id': george_info['auth_user_id'],
    })

    response1 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': george_info['auth_user_id']
    })

    user_dict = response1.json()['user']
    assert response1.status_code == 200
    assert user_dict['email'] == ''
    assert user_dict['name_first'] == 'Removed'
    assert user_dict['name_last'] == 'user'
    assert user_dict['handle_str'] == ''


# USER SETEMAIL TESTS


def test_user_setemail_invalid_token(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''

    response = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': 'invalid_token',
        'email': 'user@gmail.com',
    })
    # 403 for AccessError
    assert response.status_code == 403


def test_user_setemail_blank_email(post_test_user):
    '''
    Tests whether the proposed email is a valid email.
    '''
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


def test_user_setemail_already_exists():
    '''
    Tests for changing an email to one that is already used by another user
    '''

    requests.delete(f"{config.url}/clear/v1")
    post_bob()
    george_data = post_george()

    response = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': george_data['token'],
        'email': 'canwefixit@gmail.com'
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_setemail_successful(post_test_user):
    '''
    Asserts a successful change of email
    '''

    requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'newuseremail@gmail.com',
    })

    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': post_test_user['auth_user_id']
    })

    user_dict = response.json()['user']
    assert response.status_code == 200
    assert user_dict['email'] == 'newuseremail@gmail.com'

    bob_info = post_bob()

    response_bob = requests.put(f"{config.url}/user/profile/setemail/v1", json={
        'token': bob_info['token'],
        'email': 'bobbert@jobbery.com'
    })

    bob_profile_response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': bob_info['token'],
        'u_id': bob_info['auth_user_id']
    })

    bob_dict = bob_profile_response.json()['user']
    assert response_bob.status_code == 200
    assert bob_profile_response.status_code == 200
    assert bob_dict['email'] == 'bobbert@jobbery.com'


# USER SETHANDLE TESTS


def test_user_sethandle_invalid_token():
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{config.url}/clear/v1")

    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': 'invalid_token',
        'handle_str': 'FirstNameLastName',
    })
    # 403 for AccessError
    assert response.status_code == 403


def test_user_sethandle_short_handle(post_test_user):
    '''
    Test if handle is less than 3 characters
    '''
    # attempt to put a handle < 3 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'ew',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_long_handle(post_test_user):
    '''
    Test if handle is more than 20 characters
    '''
    # attempt to put a handle >20 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'onetwothreefourfivesix',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_non_alphanumeric(post_test_user):
    '''
    Test if handle contains non alpha-numeric characters
    '''
    # attempt to put a handle >20 characters
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'one&two',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_already_exists():
    '''
    Tests for attempting to change a handle to one that already exists
    '''
    requests.delete(f"{config.url}/clear/v1")
    post_bob()
    george_data = post_george()
    # attempt to change handle to one already in use
    # i.e. change George's handle to Bob's
    response = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': george_data['token'],
        'handle_str': 'bobbuilder'
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_sethandle_successful(post_test_user):
    '''
    Asserts a successful change of handle
    '''
    requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'coolnewhandle',
    })

    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': post_test_user['auth_user_id']
    })

    user_dict = response.json()['user']
    assert response.status_code == 200
    assert user_dict['handle_str'] == 'coolnewhandle'

    bob_info = post_bob()
    response_bob = requests.put(f"{config.url}/user/profile/sethandle/v1", json={
        'token': bob_info['token'],
        'handle_str': 'bobberino'
    })

    bob_profile_response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': bob_info['token'],
        'u_id': bob_info['auth_user_id']
    })

    bob_dict = bob_profile_response.json()['user']
    assert response_bob.status_code == 200
    assert bob_profile_response.status_code == 200
    assert bob_dict['handle_str'] == 'bobberino'


# USER SETNAME TESTS

def test_user_setname_invalid_token(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''
    response1 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': 'invalid_token',
        'name_first': 'firstname',
        'name_last': 'lastname'
    })
    # 403 for AccessError
    assert response1.status_code == 403
    response2 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': 3,
        'name_first': 'firstname',
        'name_last': 'lastname'
    })
    # 403 for AccessError
    assert response2.status_code == 403


def test_user_setname_empty(post_test_user):
    '''
    Tests if the first name and/or last name is not empty
    '''
    response1 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': '',
        'name_last': 'lastname'
    })
    # 400 for InputError
    assert response1.status_code == 400
    response2 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'firstname',
        'name_last': '',
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_user_setname_long(post_test_user):
    '''
    Tests if the first and/or last name is more than 50 characters
    '''
    # long first name > 50
    response1 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': 'lastname'
    })
    # 400 for InputError
    assert response1.status_code == 400
    # long last name > 50
    response2 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'firstname',
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    })
    # 400 for InputError
    assert response2.status_code == 400

    # both > 50
    response2 = requests.put(f"{config.url}/user/profile/setname/v1", json={
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
    # first name not a string
    response1 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 1,
        'name_last': 'lastname',
    })
    # 400 for InputError
    assert response1.status_code == 400
    # last name not a string
    response2 = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'firstname',
        'name_last': 1,
    })
    # 400 for InputError
    assert response2.status_code == 400
    # both not a string
    response1 = requests.put(f"{config.url}/user/profile/setname/v1", json={
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

    bob_info = post_bob()

    # changes user's name
    requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'New_First_Name',
        'name_last': 'New_Last_Name'
    })

    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': post_test_user['token'],
        'u_id': post_test_user['auth_user_id']
    })

    user_dict = response.json()['user']
    assert response.status_code == 200
    assert user_dict['name_first'] == 'New_First_Name'
    assert user_dict['name_last'] == 'New_Last_Name'

    response_bob = requests.put(f"{config.url}/user/profile/setname/v1", json={
        'token': bob_info['token'],
        'name_first': 'bobert',
        'name_last': 'bighteone'
    })

    bob_profile_response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': bob_info['token'],
        'u_id': bob_info['auth_user_id']
    })

    bob_dict = bob_profile_response.json()['user']
    assert response_bob.status_code == 200
    assert bob_dict['name_first'] == 'bobert'
    assert bob_dict['name_last'] == 'bighteone'
