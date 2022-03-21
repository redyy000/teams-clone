import pytest
import requests
from src import config
from tests.channel_join_v1_test import test_already_joined, test_private_channel


@pytest.fixture
def setup_users():
    requests.delete(f'{config.url}clear/v1')

    user1_info = requests.post(f'{config.url}auth/register/v2', json={'email': "dlin@gmail.com",
                                                         'password': "password",
                                                         'name_first': "daniel",
                                                         'name_last': "lin"})

    user2_info = requests.post(f'{config.url}auth/register/v2', json={'email': "rxue@gmail.com",
                                                         'password': "password",
                                                         'name_first': "richard",
                                                         'name_last': "xue"})

    user3_info = requests.post(f'{config.url}auth/register/v2', json={'email': "ryan@gmail.com",
                                                         'password': "password",
                                                         'name_first': "ryan",
                                                         'name_last': "godakanda"}

    return user1_info, user2_info, user3_info


def test_invalid_channel_id():

    user1, user2, user3=setup_users()
    requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public"
        'isPublic': True
    })

    response=requests.post(f'{config.url}/channels/join/v2', json={
        'token': user2['token'],
        'channel_id': 999999
    })

    assert response.status_code == 400

def test_already_joined():
    user1, user2, user3=setup_users()

    channel1=requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Public"
        'isPublic': True
    })

    requests.post(f'{config.url}/channels/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    response=requests.post(f'{config.url}/channels/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 400

def test_private_channel():
    user1, user2, user3=setup_users()

    channel1=requests.post(f'{config.url}/channels/create/v2', json={
        'token': user1['token'],
        'name': "Secret"
        'isPublic': False
    })

    response=requests.post(f'{config.url}/channels/join/v2', json={
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 403
