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


def test_channel_id_invalid():
    user1, user2, user3 = setup_users()
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

    response = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user1['token'],
        'channel_id': "Invalid",
        'start': 0
    })

    assert response.status_code == 400


def test_channel_index_invalid():
    user1, user2, user3 = setup_users()
    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'start': 20
    })

    response2 = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'start': -200
    })

    response3 = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'start': "String"
    })

    assert response.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400


def test_channel_member_invalid():
    user1, user2, user3 = setup_users()
    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'start': 0
    })

    assert response.status_code == 403


def test_invalid_token():
    user1, user2, user3 = setup_users()
    channel1 = requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public",
        'isPublic': True
    }).json()

    response = requests.get(f'{config.url}/channels/messages/v2', params={
        'token': "notatoken",
        'channel_id': channel1['channel_id'],
        'start': 0
    })

    assert response.status_code == 403


def test_channel_message_success():
    user1, user2, user3 = setup_users()
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

    assert requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'start': 0
    }).json() == {"messages": [], "start": 0, "end": -1}

    assert requests.get(f'{config.url}/channels/messages/v2', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'start': 0
    }).json() == {"messages": [], "start": 0, "end": -1}
