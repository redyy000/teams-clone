import pytest
import requests
from src import config


@pytest.fixture
def setup_users():
    requests.delete(f'{config.url}clear/v1')
    userlist = []
    response1 = requests.post(f'{config.url}auth/register/v2', json={'email': "dlin@gmail.com",
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
        'email': 'H11_BADGER@gmail.com'
    })

    assert auth_passwordreset_request.status_code == 200
    assert auth_passwordreset_request.json() == {}


def test_auth_passwordreset_reset_success(setup_users):
    # TODO REQUIRE FIX FOR RESET_CODE

    auth_passwordreset_request = requests.post(f'{config.url}/auth/passwordreset/request/v1', json={
        'email': 'H11_BADGER@gmail.com'
    })

    assert auth_passwordreset_request.status_code == 200
    assert auth_passwordreset_request.json() == {}

    auth_passwordreset_reset_response = requests.post(f'{config.url}auth/passwordreset/reset/v1', json={
        'reset_code': 'weghowheog',
        'new_password': 'ogwnegoineoiwg'
    })

    assert auth_passwordreset_reset_response.status_code == 200
    assert auth_passwordreset_reset_response.json() == {}
