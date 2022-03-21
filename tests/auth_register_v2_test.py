import hashlib
import jwt
from src.error import InputError, AccessError
from src import config
import pytest
import requests


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

    # Assert user is properly registered


def test_register_v2_success():

    requests.delete(f'{config.url}clear/v1')
    response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    # get user data
    assert response.status_code == 200

    '''
    data = response.json()
    # Check data is correct
    assert data[]
    '''


def test_register_v2_invalid_email():
    requests.delete(f'{config.url}clear/v1')
    response = register_user('0010101010', 'password', 'John', 'Eldenring')
    assert response.status_code == 400


def test_register_v2_existing_email():
    requests.delete(f'{config.url}clear/v1')
    register_user('john@elden.com', 'password', 'John', 'Eldenring')
    response = register_user('john@elden.com', 'password', 'James', 'Darksoul')

    assert response.status_code == 400


def test_register_v2_password_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user('john@elden.com', '123', 'John', 'Eldenring')
    assert response.status_code == 400


def test_register_v2_name_first_long():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "password",
                             "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrf", "Smith")
    assert response.status_code == 400


def test_register_v2_name_first_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "password", "", "Smith")
    assert response.status_code == 400


def test_register_v2_name_last_long():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "abc", "John",
                             "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrf")
    assert response.status_code == 400


def test_register_v2_name_last_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "abc", "John", "")
    assert response.status_code == 400
