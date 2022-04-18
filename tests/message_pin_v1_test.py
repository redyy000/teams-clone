import pytest
import requests
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


def test_invalid_token(setup_users):
    user1 = setup_users[0]
    requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": 7,
        "message_id": 4
    })
    assert pin_response.status_code == 403


def test_user_not_in_channel(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'First message of the channel!'
    })
    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'SECOND message of the channel!'
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user2['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 403


def test_invalid_message_id(setup_users):
    user1 = setup_users[0]
    requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user1['token'],
        "message_id": 4
    })
    assert pin_response.status_code == 400


def test_invalid_message_id2(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    channel = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    requests.post(f"{config.url}channel/invite/v2", json={'token': user1['token'],
                                                          'channel_id': channel.json()['channel_id'],
                                                          'u_id': user2['auth_user_id']
                                                          })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user2['token'],
        "message_id": 4
    })
    assert pin_response.status_code == 400


def test_already_pinned(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']]
    })
    requests.post(f"{config.url}message/senddm/v1", json={
        "token": user1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'First message of the dm!'
    })
    message_response = requests.post(f"{config.url}message/senddm/v1", json={
        "token": user1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'SECOND message of the dm!'
    })
    requests.post(f"{config.url}/message/pin/v1", json={
        "token": user1['token'],
        "message_id": message_response.json()['message_id']
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user1['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 400


def test_pin_with_no_owner_permissions(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    requests.post(f'{config.url}channel/invite/v2', json={
        'token': setup_users[0]['token'],
        'channel_id': channel_response.json()['channel_id'],
        'u_id': setup_users[1]['auth_user_id']
    })
    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'First message of the channel!'
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user2['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 403


def test_pin_with_no_owner_permissions2(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']]
    })
    message_response = requests.post(f"{config.url}message/senddm/v1", json={
        "token": user1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'First message of the dm!'
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user2['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 403


def test_pin_success(setup_users):
    user1 = setup_users[0]
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1['token'],
        "name": "general",
        "is_public": True
    })
    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'First message of the channel!'
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user1['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 200
    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': user1['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })
    assert messages_response.json()['messages'][0]['is_pinned'] == True


def test_pin_with_no_owner_permissions3(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']]
    })
    message_response = requests.post(f"{config.url}message/senddm/v1", json={
        "token": user1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'First message of the dm!'
    })
    pin_response = requests.post(f"{config.url}/message/pin/v1", json={
        "token": user2['token'],
        "message_id": message_response.json()['message_id']
    })
    assert pin_response.status_code == 403
