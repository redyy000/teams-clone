import pytest
import requests
from src import config


@pytest.fixture
def post_test_user():
    return test_user()


def test_user():
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


@pytest.fixture
def post_dm_create():
    post_info = test_user()
    george_info = post_george()
    bob_info = post_bob()
    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_info['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    return post_info


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


def test_dm_remove_successful(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    remove_response = requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': post_test_user['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    assert remove_response.status_code == 200

    # Should return an InputError, as DM is fully deleted
    # The dm_id no longer exists.
    dm_details = requests.get(f"{config.url}/dm/details/v1", params={
        'token': george_info['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    assert dm_details.status_code == 400


def test_dm_remove_invalid_token(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    remove_response = requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': 'false token',
        'dm_id': dm_info.json()['dm_id']
    })

    assert remove_response.status_code == 403


def test_dm_remove_no_dm(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    remove_response = requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': post_test_user['token'],
        'dm_id': 9999999999
    })

    assert remove_response.status_code == 400


def test_dm_remove_non_creator(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    remove_response = requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': bob_info['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    assert remove_response.status_code == 403


def test_dm_remove_non_member(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [bob_info['auth_user_id']]
    })

    remove_response = requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': george_info['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    assert remove_response.status_code == 403
