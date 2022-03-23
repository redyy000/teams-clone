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


def create_dm(token, u_ids):

    return requests.post(f'{config.url}dm/create/v1', json={
        'token': token,
        'u_ids': u_ids
    })


def test_dm_list_successful(post_dm_create):

    dm_list_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': post_dm_create['token']
    })

    assert dm_list_response.status_code == 200

# Could be blackboxed....
# Assumes list of dm_ids...

# WRONG
# List of dictionaries, where each dictionary contains types { dm_id, name }


def test_dm_list_multiple_dms(post_test_user):

    george_info = post_george()
    bob_info = post_bob()

    create_dm(post_test_user['token'], [
        bob_info['auth_user_id'], george_info['auth_user_id']])
    create_dm(post_test_user['token'], [bob_info['auth_user_id']])
    create_dm(post_test_user['token'], [george_info['auth_user_id']])

    dm1_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': post_test_user['token']
    })

    assert dm1_response.status_code == 200
    assert dm1_response.json() == {
        'dms': [{
            'dm_id': 1,
            'name': 'bobbuilder, firstnamelastname, georgemonkey'
        },
            {
            'dm_id': 2,
            'name': 'bobbuilder, firstnamelastname'
        },
            {
            'dm_id': 3,
            'name': 'firstnamelastname, georgemonkey'
        }
        ]
    }

    dm2_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': bob_info['token']
    })

    assert(dm2_response.status_code) == 200
    assert dm2_response.json() == {
        'dms': [{
            'dm_id': 1,
            'name': 'bobbuilder, firstnamelastname, georgemonkey'
        },
            {
            'dm_id': 2,
            'name': 'bobbuilder, firstnamelastname'
        },
        ]
    }

    dm3_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': george_info['token']
    })

    assert(dm3_response.status_code) == 200
    assert dm3_response.json() == {
        'dms': [{
            'dm_id': 1,
            'name': 'bobbuilder, firstnamelastname, georgemonkey'
        },
            {
            'dm_id': 3,
            'name': 'firstnamelastname, georgemonkey'
        }
        ]
    }


def test_dm_list_invalid_token(post_dm_create):

    dm_list_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': 'false token'
    })

    assert dm_list_response.status_code == 403

# Empty case??


def test_dm_list_no_dms(post_dm_create):

    lonely_info = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'no_friends@sad.com',
        'password': 'oeihoihwoihoih',
        'name_first': 'life',
        'name_last': 'isverylong',
    }).json()

    dm_list_response = requests.get(f'{config.url}dm/list/v1', params={
        'token': lonely_info['token']
    })

    assert dm_list_response.status_code == 200
    assert dm_list_response.json() == {'dms': []}
