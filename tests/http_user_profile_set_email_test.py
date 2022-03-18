from platformdirs import user_cache_dir
import pytest
import requests
import json
import urllib

'''
Test functions for user_profile_setemail_v1. Tests for:
    - Invalid user (token invalid)
    - Set current email to blank/empty email
    - Set current to invalid email
    - Email already being used by another user
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


def test_invalid_user(post_test_user):
    '''
    Tests if user token is valid i.e. if user exists
    '''
    requests.delete(f"{url}/clear/v1")

    response = requests.get(f"{url}/user/profile/setemail/v1", json={
        'token': 'invalid_token',
        'email': 'user@gmail.com',
    })
    # 400 for InputError
    assert response.status_code == 400


def test_blank_email(post_test_user):
    '''
    Tests whether the proposed email is a valid email.
    '''
    requests.delete(f"{url}/clear/v1")

    # attempt to put a blank email
    response = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],  # finds the token of user
        'email': '',  # attempts to set email to a blank email
    })
    # 400 for InputError
    assert response.status_code == 400


def test_invalid_email(post_test_user):
    '''
    Tests whether the email is in the correct email format, i.e. is a valid email
    '''
    requests.delete(f"{url}/clear/v1")

    # attempt to put an invalid email, no @
    response1 = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'invalid.com',
    })
    # 400 for InputError
    assert response1.status_code == 400


# attempt to put an invalid emial, no .com
    response2 = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'invalid@gmail',
    })
    # 400 for InputError
    assert response2.status_code == 400


def test_email_already_exists(post_george, post_bob):
    '''
    Tests for changing an email to one that is already used by another user
    '''
    requests.delete(f"{url}/clear/v1")
    # attempt to change email to one already in use
    # i.e. change George's email to Bob's
    response = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': post_george['token'],
        'email': post_bob['email'],
    })
    # 400 for InputError
    assert response.status_code == 400


def test_user_profile_setemail_successful(post_test_user):
    '''
    Asserts a successful change of email
    '''
    requests.delete(f"{url}/clear/v1")
    # changes user['email']
    requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': post_test_user['token'],
        'email': 'newuseremail@gmail.com',
    })
    assert post_test_user['email'] == 'newuseremail@gmail.com'
