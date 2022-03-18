from platformdirs import user_cache_dir
import pytest

import requests
import json
import urllib

'''
Test functions for user_profile_setname_v1. Tests for:
    - Invalid user (token invalid)
    - Setting empty name
    - Setting a name that is too long
    - Setting a name that is not a string
    - user_profile_setname_v1 is successful at changing a user's name
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


def test_invalid_user(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{url}/clear/v1")
    response1 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': 'invalid_token',
        'name_first': post_test_user['name_first'],
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response1.status_code == 400
    response2 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': 3,
        'name_first': post_test_user['name_first'],
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_blank_setname(post_test_user):
    '''
    Tests if the first name and/or last name is not empty
    '''
    requests.delete(f"{url}/clear/v1")
    response1 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': '',
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response1.status_code == 400
    response2 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': '',
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_long_setname(post_test_user):
    '''
    Tests if the first and/or last name is more than 50 characters
    '''
    requests.delete(f"{url}/clear/v1")
    # long first name > 50
    response1 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': post_test_user['name_last']
    })
    # 400 for InputError
    assert response1.status_code == 400
    # long last name > 50
    response2 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    })
    # 400 for InputError
    assert response2.status_code == 400

    # both > 50
    response2 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_setname_not_string(post_test_user):
    '''
    Tests if the name entered is a string
    '''
    requests.delete(f"{url}/clear/v1")
    # first name not a string
    response1 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 1,
        'name_last': post_test_user['name_last'],
    })
    # 400 for InputError
    assert response1.status_code == 400
    # last name not a string
    response2 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': post_test_user['name_first'],
        'name_last': 1,
    })
    # 400 for InputError
    assert response2.status_code == 400
    # both not a string
    response1 = requests.get(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 1,
        'name_last': 1,
    })
    # 400 for InputError
    assert response1.status_code == 400


def test_setname_successful(post_test_user):
    '''
    Tests if user_profile_setname_v1
    '''
    requests.delete(f"{url}/clear/v1")
    # changes user's name
    requests.put(f"{url}/user/profile/setname/v1", json={
        'token': post_test_user['token'],
        'name_first': 'New_First_Name',
        'name_last': 'New_Last_Name'
    })
    assert post_test_user['name_first'] == 'New_First_Name'
    assert post_test_user['name_last'] == 'New_Last_Name'
