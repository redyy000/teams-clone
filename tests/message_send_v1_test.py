import pytest
import requests
# from setuptools import setup
from src import config


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


def test_message_send_success(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response1 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    message_response2 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every john has its burger'
    })

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    assert message_response1.status_code == 200
    assert message_response2.status_code == 200
    assert message_response3.status_code == 200


def test_message_send_multiple_channels(setup_users):
    owner = setup_users[0]

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    channel_response2 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "minutes",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response2.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    assert message_response.status_code == 200


def test_message_send_invalid_token(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": 'hwgowehgiowehgoihwoiehg',
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    assert message_response.status_code == 403


def test_message_send_invalid_channel_id(setup_users):

    owner = setup_users[0]

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": 999999999999,
        "message": 'Every soul has its dark'
    })

    assert message_response.status_code == 400


def test_message_send_message_length_short(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": ''
    })

    assert message_response.status_code == 400


def test_message_send_message_length_long(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark' * 250
    })

    assert message_response.status_code == 400


def test_message_send_unauthorised_user(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": member1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    assert message_response.status_code == 403


def test_message_send_multiple_users(setup_users):
    # create the channel
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": setup_users[0]['token'],
        "name": "Jungle",
        "is_public": True
    })
    assert channel_response.status_code == 200
    channel_id = channel_response.json()['channel_id']

    # invite all users to channel
    invite_user1 = requests.post(f'{config.url}channel/invite/v2', json={
        'token': setup_users[0]['token'],
        'channel_id': channel_id,
        'u_id': setup_users[1]['auth_user_id']
    })
    assert invite_user1.status_code == 200

    invite_user2 = requests.post(f'{config.url}channel/invite/v2', json={
        'token': setup_users[0]['token'],
        'channel_id': channel_id,
        'u_id': setup_users[2]['auth_user_id']
    })
    assert invite_user2.status_code == 200
    # send messages between members
    user_2_message = requests.post(f"{config.url}message/send/v1", json={
        "token": setup_users[2]['token'],
        "channel_id": channel_id,
        "message": 'Welcome to the jungle.'
    })
    assert user_2_message.status_code == 200

    message_id1 = user_2_message.json()['message_id']
    assert message_id1 == 1

    user_1_message = requests.post(f"{config.url}message/send/v1", json={
        "token": setup_users[1]['token'],
        "channel_id": channel_id,
        "message": "We've got fun and games"
    })
    assert user_1_message.status_code == 200

    message_id2 = user_1_message.json()['message_id']
    assert message_id2 == 2
