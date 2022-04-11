import pytest
import requests
from src import config


@pytest.fixture
def setup_users():
    requests.delete(f'{config.url}clear/v1')
    userlist = []
    response1 = requests.post(f'{config.url}auth/register/v2', json={'email': "h11abadger@gmail.com",
                                                                     'password': "password",
                                                                     'name_first': "daniel",
                                                                     'name_last': "lin"})

    response2 = requests.post(f'{config.url}auth/register/v2', json={'email': "rxue@gmail.com",
                                                                     'password': "password",
                                                                     'name_first': "richard",
                                                                     'name_last': "xue"})

    response3 = requests.post(f'{config.url}auth/register/v2', json={'email': "ryan@gmail.com",
                                                                     'password': "password",
                                                                     'name_first': "ryan",
                                                                     'name_last': "godakanda"})

    user1_info = (response1.json())
    user2_info = (response2.json())
    user3_info = (response3.json())
    userlist.append(user1_info)
    userlist.append(user2_info)
    userlist.append(user3_info)
    return userlist


def test_auth_passwordreset_request_success(setup_users):
    auth_passwordreset_request = requests.post(f'{config.url}/auth/passwordreset/request/v1', json={
        'email': 'h11abadger@gmail.com'
    })

    assert auth_passwordreset_request.status_code == 200
    assert auth_passwordreset_request.json() == {}


# Used for testing purposes
# In reality, reset_code is randomised; hence pytest will not work
# Used dummy reset_code to test this works.
'''
def test_auth_passwordreset_reset_success(setup_users):
   

    auth_passwordreset_request = requests.post(f'{config.url}/auth/passwordreset/request/v1', json={
        'email': 'h11abadger@gmail.com'
    })

    assert auth_passwordreset_request.status_code == 200
    assert auth_passwordreset_request.json() == {}

    auth_passwordreset_reset_response = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'reset_code',
        'new_password': 'new_password'
    })

    assert auth_passwordreset_reset_response.status_code == 200
    assert auth_passwordreset_reset_response.json() == {}

    # Try to login
    login_response = requests.post(f'{config.url}auth/login/v2', json={'email': 'h11abadger@gmail.com',
                                                                       'password': 'new_password'})

    assert(login_response.status_code) == 200
'''


# Test that a reset code is removed

'''
def test_auth_passwordreset_reset_success(setup_users):
   

    auth_passwordreset_request = requests.post(f'{config.url}/auth/passwordreset/request/v1', json={
        'email': 'h11abadger@gmail.com'
    })

    assert auth_passwordreset_request.status_code == 200
    assert auth_passwordreset_request.json() == {}

    auth_passwordreset_reset_response = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'reset_code',
        'new_password': 'new_password'
    })

    assert auth_passwordreset_reset_response.status_code == 200
    assert auth_passwordreset_reset_response.json() == {}

    # Try to login
    login_response = requests.post(f'{config.url}auth/login/v2', json={'email': 'h11abadger@gmail.com',
                                                                       'password': 'new_password'})

    assert(login_response.status_code) == 200
    
    
    # Try to login with invalid reset code
    auth_passwordreset_reset_response_fail = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'reset_code',
        'new_password': 'new_password'
    })
    
    assert auth_passwordreset_reset_response_fail.status_code = 400
'''


def test_auth_passwordreset_reset_short(setup_users):
    auth_passwordreset_reset_response = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'reset_code',
        'new_password': 'eee'
    })

    assert auth_passwordreset_reset_response.status_code == 400


def test_auth_passwordreset_reset_false_code(setup_users):
    auth_passwordreset_reset_response = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'lmao this does"wg',
        'new_password': 'ekjgeog'
    })

    assert auth_passwordreset_reset_response.status_code == 400
