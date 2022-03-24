import pytest
import requests
from src import config

'''
    Given a u_id, remove the user from Seams.
    Check that:
    - User removed from all channels/dms
    - User not in users list
    - Message contents replaced by 'Removed User'
    - 'name_first': 'Removed'
    - 'name_last': 'user'
    - Email and handle should be reusable 
'''


@pytest.fixture
def global_george():
    '''
    Creates test user named George Monkey, email george@gmail.com.
    '''
    george = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': 'monkey',
        'name_first': 'George',
        'name_last': 'Monkey',
    })
    george_data = george.json()
    return george_data


@pytest.fixture
def user_bob():
    '''
    Creates test user named Bob Builder, email canwefixit@gmail.com .
    '''
    bob = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'canwefixit@gmail.com',
        'password': 'yeswecan',
        'name_first': 'Bob',
        'name_last': 'Builder',
    })
    bob_data = bob.json()
    return bob_data


@pytest.fixture
def user_snape():
    '''
    Creates test user named Severus Snape, email halfbloodprince@gmail.com .
    '''
    snape = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'halfbloodprince@gmail.com',
        'password': 'sectumsempra',
        'name_first': 'Severus',
        'name_last': 'Snape',
    })
    snape_data = snape.json()
    return snape_data


def test_admin_user_remove_v1_success(global_george, user_bob, user_snape):
    '''
    firstly, test admin/user/remove returns 200
    '''
    # Create a global owner and member
    requests.delete(f"{config.url}/clear/v1")

    # Global_owner_george creates a channel
    channel = requests.post(f"{config.url}channels/create/v2", json={
        "token": global_george['token'],
        "name": "Welcome to Seams",
        "is_public": True
    }).json

    # global_owner_george invites Bob to the channel
    requests.post(f'{config.url}channel/invite/v2', json={
        'token': global_george['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_bob['auth_user_id']
    })

    # user_bob sends a message
    new_message = requests.post(f"{config.url}message/send/v1", json={
        'token': user_bob['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hi George!'
    })
    assert new_message.status_code == 200

    # user_bob also sends a dm
    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': user_bob['token'],
        'u_ids': [global_george['auth_user_id'], user_snape['auth_user_id']]
    })
    new_dm = requests.post(f'{config.url}message/senddm/v1', json={
        'token': user_bob['token'],
        'dm_id': dm_id.json()['dm_id'],
        'message': "Hello World"})

    assert dm_id.status_code == 200
    assert new_dm.status_code == 200

    # user_bob gets removed from seams by global owner george
    remove_bob = requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': global_george['token'],
        'u_id': user_bob['auth_user_id']
    })
    assert remove_bob.status_code == 200

    # so messages become 'Removed user'

    assert new_message['message'] == 'Removed user'
    assert new_dm['message'] == 'Removed user'


def test_admin_user_remove_v1_user_removed_from_channel(global_george, user_bob):
    # Assert user no longer in users list

    requests.delete(f"{config.url}/clear/v1")

    channel = requests.post(f"{config.url}channels/create/v2", json={
        "token": global_george['token'],
        "name": "Welcome to Seams",
        "is_public": True
    }).json

    remove_bob = requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': global_george['token'],
        'u_id': user_bob['auth_user_id']
    })
    assert remove_bob.status_code == 200

    assert channel['all_members'] == {
        'u_id': global_george['auth_user_id'],
        'email': 'george@gmail.com',
        'name_first': 'George',
        'name_last': 'Monkey',
        'handle_str': 'georgemonkey',

    }


def test_admin_user_remove_v1_user_removed_from_dm(global_george, user_bob, user_snape):
    requests.delete(f"{config.url}/clear/v1")

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': user_bob['token'],
        'u_ids': [global_george['auth_user_id'], user_snape['auth_user_id']]
    })
    assert dm_id.status_code == 200

    remove_snape = requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': global_george['token'],
        'u_id': user_snape['auth_user_id']
    })
    assert remove_snape.status_code == 200
    assert dm_id['u_ids'] == [global_george['auth_user_id']]


def test_admin_user_remove_v1_user_removed_from_user_list(global_george, user_george, user_snape):
    requests.delete(f"{config.url}/clear/v1")

    # remove snape
    requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': global_george['token'],
        'u_id': user_snape['auth_user_id']
    })

    # attempt to access dm_details with now invalid user, input error
    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': global_george['token'],
        'u_ids': [user_george['auth_user_id']]
    })
    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': user_snape['token'],
        'dm_id': dm_id.json()['dm_id']
    })

    assert dm_details.status_code == 400


def test_admin_user_remove_v1_name_now_removed_user(global_george, user_bob):
    '''
    Tests that user 'name_first' == 'Removed', 'name_last' == 'user'
    '''
    requests.delete(f"{config.url}/clear/v1")
    # user_bob gets removed from seams
    create_global = global_george
    create_user = user_bob

    remove_bob = requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': create_global['token'],
        'u_id': create_user['auth_user_id']
    })
    assert remove_bob.status_code == 200
    assert user_bob['name_first'] == 'Removed'
    assert user_bob['name_last'] == 'user'


def test_admin_user_remove_v1_invalid_user(global_george):
    '''
    Attempting to remove invalid user
    '''
    requests.delete(f"{config.url}/clear/v1")

    remove_invalid_user = requests.delete(f'{config.url}/admin/user/remove/v1', json={
        'token': global_george['token'],
        'u_id': 'invalid_auth_user_id'
    })
    assert remove_invalid_user.status_code == 400


def test_admin_user_remove_v1_only_global_owner(global_george):
    '''
    Access error when attempting to remove the only global owner
    '''
    requests.delete(f"{config.url}/clear/v1")

    remove_george = requests.delete(f'{config.url}dm/create/v1', json={
        'token': global_george['token'],
        'u_id': global_george['auth_user_id']
    })
    assert remove_george.status_code == 403
