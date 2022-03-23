import hashlib
import jwt
import pytest
import requests
from src import config


@pytest.fixture
# Returns a JSON file with status code and data
def initialise_test():
    '''
    Pytest fixture function to clear all records, and return a dummy user
    For testing purposes 
    '''
    # Calls clear on the saved data server-side
    requests.delete(f'{config.url}clear/v1')

    response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    return response


def register_user(email, password, name_first, name_last):
    '''
    Creates and sends a post request 

    Arguments:
        email (string)    - Email string that accepts regular expression
        password (string)    - Password for the email address, 6 or more characters long.
        name_first (string) - String containing first name, between 1-50 characters inclusive.
        name_last (string) - String containing last name, between 1-50 characters inclusive.

    Exceptions:
        None

    Return Value:
        {'username' : string } dictionary
    '''

    return requests.post(f'{config.url}auth/register/v2', json={'email': email,
                                                                'password': password,
                                                                'name_first': name_first,
                                                                'name_last': name_last})


def test_logout_success(initialise_test):
    data = initialise_test.json()
    token = data['token']
    logout_response = requests.post(
        f'{config.url}auth/logout/v1', json={'token': token})

    assert(logout_response.status_code) == 200

    # Logout with an invalid token


def test_logout_success_multiple(initialise_test):

    register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    user2 = register_user('John@ring.com', 'password', 'John', 'Eldenring')

    user0_token = initialise_test.json()['token']
    logout_response1 = requests.post(
        f'{config.url}auth/logout/v1', json={'token': user0_token})

    assert(logout_response1.status_code) == 200

    logout_response2 = requests.post(
        f'{config.url}auth/logout/v1', json={'token': user2.json()['token']})

    assert(logout_response2.status_code) == 200


def test_logout_login_success(initialise_test):

    login1 = requests.post(f'{config.url}auth/login/v2', json={'email': 'Elden@ring.com',
                                                               'password': 'password'})

    login2 = requests.post(f'{config.url}auth/login/v2', json={'email': 'Elden@ring.com',
                                                               'password': 'password'})

    # Logout of login2
    logout_response2 = requests.post(
        f'{config.url}auth/logout/v1', json={'token': login2.json()['token']})

    assert logout_response2.status_code == 200

    # Logout of login1
    logout_response1 = requests.post(
        f'{config.url}auth/logout/v1', json={'token': login1.json()['token']})

    assert logout_response1.status_code == 200


def test_logout_fail(initialise_test):
    # Access Error
    logout_response = requests.post(
        f'{config.url}auth/logout/v1', json={'token': 'incredibly fake token'})

    assert(logout_response.status_code) == 403
