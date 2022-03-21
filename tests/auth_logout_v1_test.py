import hashlib
import jwt
import pytest
import requests
from src.error import InputError
from src import auth
from src.other import clear_v1
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
    
    return requests.post(f'{config.url}auth/register/v2', json = {'email'      : email,
                                                           'password'   : password,
                                                           'name_first' : name_first,
                                                           'name_last'  : name_last})
    
    # Should write more....
def test_logout_success(initialise_test):
    data = initialise_test.get_json
    token = data['token']
    logout_response = requests.post(f'{config.url}auth/logout/v1', json = {'token' : token})
    
    assert(logout_response) == 200
    
    
    # No failure cases? 
    # No real exceptions given in README
    
def test_logout_fail(initialise_test):
    '''
    data = initialise_test.get_json
    token = data['token']
    '''
    pass
