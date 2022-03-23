import pytest
import requests
from src import config
import json


@pytest.fixture
def setup_users():
    requests.delete(f'{config.url}clear/v1')

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
    return user1_info, user2_info, user3_info


def test_invalid_channel_id():

    user1, user2, user3 = setup_users()
    requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    })

    response = requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': 999999
    })

    assert response.status_code == 400


def test_already_joined():
    user1, user2, user3 = setup_users()

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    response = requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 400


def test_private_channel():
    user1, user2, user3 = setup_users()

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Secret",
        'isPublic': False
    }).json()

    response = requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 403


def test_successful_join():
    user1, user2, user3 = setup_users()

    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })
    response2 = requests.post(f'{config.url}/channel/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    requests.get(f'{config.url}/channel/join/v2', params={
        'token': user2['token']
    })

    assert response.status_code == 200 and response2.status_code == 200
    assert requests.get(f'{config.url}channels/list/v2', params={
        user2['token']}).json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}

    assert requests.get(f'{config.url}channels/list/v2', params={
        user3['token']}).json() == {'channels': [{"channel_id": channel1["channel_id"], "name": "Public"}]}


def test_invalid_token():
    user1, user2, user3 = setup_users()

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
