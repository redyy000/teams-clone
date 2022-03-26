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

    for member_dict in dm_details.json()['members']:
        if member_dict['u_id'] == post_test_user['auth_user_id']:
            assert member_dict['email'] == "user@gmail.com"
            assert member_dict['name_first'] == "FirstName"
            assert member_dict['name_last'] == "LastName"
            assert member_dict['handle_str'] == "firstnamelastname"
        if member_dict['u_id'] == bob_info['auth_user_id']:
            assert member_dict['email'] == "canwefixit@gmail.com"
            assert member_dict['name_first'] == "Bob"
            assert member_dict['name_last'] == "Builder"
            assert member_dict['handle_str'] == "bobbuilder"
        if member_dict['u_id'] == george_info['auth_user_id']:
            assert member_dict['email'] == "george@gmail.com"
            assert member_dict['name_first'] == "George"
            assert member_dict['name_last'] == "Monkey"
            assert member_dict['handle_str'] == "georgemonkey"


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

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_response.json()['dm_id']
    })

    assert dm_details.status_code == 200
    assert dm_details.json()[
        'name'] == 'firstnamelastname'

    for member_dict in dm_details.json()['members']:
        if member_dict['u_id'] == post_test_user['auth_user_id']:
            assert member_dict['email'] == "user@gmail.com"
            assert member_dict['name_first'] == "FirstName"
            assert member_dict['name_last'] == "LastName"
            assert member_dict['handle_str'] == "firstnamelastname"


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
