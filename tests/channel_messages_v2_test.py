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

    user1_info = response1.json()
    user2_info = response2.json()
    user3_info = response3.json()
    userlist.append(user1_info)
    userlist.append(user2_info)
    userlist.append(user3_info)
    return userlist


def test_channel_id_invalid(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'u_id': setup_users[1]['auth_user_id']
    })

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': "Invalid",
        'start': 0
    })

    assert response.status_code == 400


def test_channel_index_invalid(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'start': 20
    })

    response2 = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'start': -200
    })

    response3 = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'start': "String"
    })

    assert response.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400


def test_channel_member_invalid(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': "sfsjfkjksfj",
        'channel_id': channel1['channel_id'],
        'start': 0
    })

    assert response.status_code == 403


def test_invalid_token(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': "notatoken",
        'channel_id': channel1['channel_id'],
        'start': 0
    })

    assert response.status_code == 403


def test_channel_message_success(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'u_id': setup_users[1]['auth_user_id']
    })

    response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': setup_users[1]['token'],
        'channel_id': channel1['channel_id'],
        'start': 0
    })
    assert response.status_code == 200
    assert response.json() == {"messages": [], "start": 0, "end": -1}

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel1['channel_id'],
        'start': 0
    })
    assert response.status_code == 200
    assert response.json() == {"messages": [], "start": 0, "end": -1}
