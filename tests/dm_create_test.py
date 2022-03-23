import pytest
import requests
from src import config


@pytest.fixture
def post_test_user():
    requests.delete(f"{config.url}/clear/v1")
    '''
    Creates a test user and posts for use in http testing.
    '''
    post_test_user = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'user@gmail.com',
        'password': 'password',
        'name_first': 'FirstName',
        'name_last': 'LastName',
    })
    user_data = post_test_user.json()
    return user_data


def post_george():
    '''
    Creates test user named George Monkey, email george@gmail.com.
    '''
    post_george = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': 'monkey',
        'name_first': 'George',
        'name_last': 'Monkey',
    })
    george_data = post_george.json()
    return george_data


def post_bob():
    '''
    Creates test user named Bob Builder, email canwefixit@gmail.com .
    '''
    post_bob = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'canwefixit@gmail.com',
        'password': 'yeswecan',
        'name_first': 'Bob',
        'name_last': 'Builder',
    })
    bob_data = post_bob.json()
    return bob_data

# DM_CREATE_TESTS


def test_dm_create_successful(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    assert dm_response.status_code == 200


def test_dm_create_functionality(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_response.json()['dm_id']
    })

    assert dm_response.status_code == 200
    assert dm_details.status_code == 200
    assert dm_details.json()[
        'name'] == 'bobbuilder, firstnamelastname, georgemonkey'
    assert bob_info['auth_user_id'] in dm_details.json()['members']
    assert post_test_user['auth_user_id'] in dm_details.json()['members']
    assert george_info['auth_user_id'] in dm_details.json()['members']


def test_dm_create_invalid_token(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': 'false token',
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    assert dm_response.status_code == 403


def test_dm_create_empty_u_ids(post_test_user):

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': []
    })

    assert dm_response.status_code == 200


def test_dm_create_invalid_u_id(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id'], 99999]
    })

    assert dm_response.status_code == 400


def test_dm_create_duplicate_u_ids(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id'], george_info['auth_user_id'], george_info['auth_user_id']]
    })

    assert dm_response.status_code == 400
