

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
    print("Posting auth register request!")
    return requests.post(f'{config.url}/auth/register/v2', json={'email': email,
                                                                 'password': password,
                                                                 'name_first': name_first,
                                                                 'name_last': name_last})

    # Assert user is properly registered


if __name__ == "__main__":
    requests.delete('/clear/v1')
    print("SENDING")
    response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    # print(response.json())
    # print(response.json()['auth_user_id'])
