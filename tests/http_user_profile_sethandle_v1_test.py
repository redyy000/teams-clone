from platformdirs import user_cache_dir
import pytest
from src.error import InputError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.server import user_profile_sethandle_v1

import requests
import json
import urllib

'''
Test functions for user_profile_sethandle_v1. Tests for:
    - Invalid user (token invalid)
    - Setting handle less than 3 characters
    - Setting handle more than 20 characters
    - Handle containing non-alphanumeric characters
    - Handle already used
    - user_profile_sethandle_v1 is successful at changing a user's handle
'''
port = 8080

url = f"http://localhost:{port}/"


@pytest.fixture
def post_test_user():
    '''
    Creates a test user and posts for use in http testing. 
    '''
    post_test_user = requests.post(f"{url}/auth/register/v2", json={
        'email': 'user@gmail.com',
        'password': hash('password'),
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
    post_george = requests.post(f"{url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': hash('monkey'),
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
    post_bob = requests.post(f"{url}/auth/register/v2", json={
        'email': 'canwefixit@gmail.com',
        'password': hash('yeswecan'),
        'name_first': 'Bob',
        'name_last': 'Builder',
    })
    bob_data = post_bob.json()
    return bob_data


def test_invalid_user():
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{url}/clear/v1")

    response = requests.get(f"{url}/user/profile/sethandle/v1", json={
        'token': 'invalid_token',
        'handle_str': 'FirstNameLastName',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_short_handle(post_test_user):
    '''
    Test if handle is less than 3 characters
    '''
    requests.delete(f"{url}/clear/v1")
    # attempt to put a handle < 3 characters
    response = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'ew',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_long_handle():
    '''
    Test if handle is more than 20 characters
    '''
    requests.delete(f"{url}/clear/v1")
    # attempt to put a handle >20 characters
    response = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'onetwothreefourfivesix',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_handle_non_alphanumeric():
    '''
    Test if handle contains non alpha-numeric characters
    '''
    requests.delete(f"{url}/clear/v1")
    # attempt to put a handle >20 characters
    response = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'one&two',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_handle_already_exists(post_george, post_bob):
    '''
    Tests for attempting to change a handle to one that already exists
    '''
    requests.delete(f"{url}/clear/v1")
    # attempt to change handle to one already in use
    # i.e. change George's handle to Bob's
    response = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': post_george['token'],
        'handle_str': post_bob['handle_str'],
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_profile_sethandle_successful():
    '''
    Asserts a successful change of handle
    '''
    requests.delete(f"{url}/clear/v1")
    response = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': post_test_user['token'],
        'handle_str': 'coolnewhandle',
    })
    assert post_test_user['handle_str'] == 'coolnewhandle'
