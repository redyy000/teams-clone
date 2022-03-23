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


def test_invalid_channel_id(setup_users):

    requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    })
    response = requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': 999999
    })

    assert response.status_code == 400


def test_already_joined(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': channel1['channel_id']
    })

    response = requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 400


def test_private_channel(setup_users):

    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Secret",
        'is_public': False
    }).json()

    response = requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 403


def test_successful_join(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()
    requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "GITLAB",
        'is_public': True
    }).json()
    requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': channel1['channel_id']
    })

    requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[2]['token'],
        'channel_id': channel1['channel_id']
    })

    response = requests.get(f'{config.url}channels/list/v2', params={"token":
        setup_users[1]['token']})
    assert response.status_code == 200
    assert response.json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}
    
    response = requests.get
    response = requests.get(f'{config.url}channels/list/v2', params={"token":
        setup_users[2]['token']})
    assert response.status_code == 200
    assert response.json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}


def test_invalid_token(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    response = requests.post(f'{config.url}channel/join/v2', json={
        'token': 'WRONGTOKENNNN',
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 403
