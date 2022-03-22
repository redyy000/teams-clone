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


'''
Login:
Return Type:{ token, auth_user_id }
'''


def test_login_success(initialise_test):

    login_response = requests.post(f'{config.url}auth/login/v2', json={'email': 'Elden@ring.com',
                                                                       'password': 'password'})

    assert(login_response.status_code) == 200

    # Functionality test
    assert login_response.json(
    )['auth_user_id'] == initialise_test.json()['auth_user_id']


def test_login_email_fail(initialise_test):

    login_response = requests.post(f'{config.url}auth/login/v2', json={'email': 'Dark@soul.com',
                                                                       'password': 'password'})
    assert(login_response.status_code) == 400


def test_login_password_fail(initialise_test):

    login_response = requests.post(f'{config.url}auth/login/v2', json={'email': 'Elden@ring.com',
                                                                       'password': 'WRONG'})

    assert(login_response.status_code) == 400
