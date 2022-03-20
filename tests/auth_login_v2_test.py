import hashlib
import jwt
import pytest
import requests
from src.error import InputError
from src import auth
from src.other import clear_v1
from src import config


@pytest.fixture


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
    
def test_login_success():
    
    requests.delete(f'{config.url}clear/v1')
    register_response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    login_response = requests.post(f'{config.url}auth/login/v2', json = {'email' : 'Elden@ring.com',
                                                                         'password' : 'password'})
    
    assert(login_response.status_code) == 200
# 
def test_login_email_fail():
    requests.delete(f'{config.url}clear/v1')
    login_response = requests.post(f'{config.url}auth/login/v2', json = {'email' : 'Elden@ring.com',
                                                                         'password' : 'password'})
    assert(login_response.status_code) == 400
    
    
def test_login_password_fail():
    
    requests.delete(f'{config.url}clear/v1')
    register_response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    login_response = requests.post(f'{config.url}auth/login/v2', json = {'email' : 'Elden@ring.com',
                                                                         'password' : 'WRONG'})
    
    assert(login_response.status_code) == 400
