import pytest
import requests
from src import config
import json


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

    user1_info = json.loads(response1.json())
    user2_info = json.loads(response2.json())
    user3_info = json.load(response3.json())
    userlist.extend(user1_info, user2_info, user3_info)
    return userlist


def test_invalid_channel_id(setup_users):

    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]
    requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    })

    response = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': 999999,
        'u_id': user2['auth_user_id']
    })

    assert response.status_code == 400


def test_invalid_uid(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]
    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': "blah blah"
    })

    assert response.status_code == 400


def test_already_a_member(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['auth_user_id']
    })

    response = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['auth_user_id']
    })

    assert response.status_code == 400


def test_unauthorised(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user3['auth_user_id']
    })

    assert response.status_code == 403


def test_invalid_token(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    })

    response = requests.post(f'{config.url}/channel/join/v2', json={
        'token': 'WRONGTOKENNNN',
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 403


def test_successful_invite(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]
    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['auth_user_id']
    })

    response2 = requests.post(f'{config.url}/channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user3['auth_user_id']
    })

    assert requests.get(f'{config.url}channels/list/v2', params={
        'token': user2['token']}).json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}

    assert requests.get(f'{config.url}channels/list/v2', params={
        'token': user3['token']}).json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}

    assert response.status_code == 200 and response2.status_code == 200