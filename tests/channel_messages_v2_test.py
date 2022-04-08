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


def test_invalid_user(setup_users):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    }).json()

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': setup_users[1]['token'],
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


def test_channel_message_success_functionality(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': "Public",
        'is_public': True
    }).json()

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response['channel_id'],
        "message": 'Every soul has its dark'
    })

    # Send some messages

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_response['channel_id'],
        'start': 0
    })

    assert response.status_code == 200
    assert response.json()['start'] == 0
    assert response.json()['end'] == -1
    assert len(response.json()['messages']) == 1
    assert response.json()[
        'messages'][0]['message'] == 'Every soul has its dark'
    assert response.json()['messages'][0]['message_id'] == 1


def test_channel_messages_functionality_125(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': 'general',
        'is_public': True
    })

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel_id.json()['channel_id'],
        'u_id': member1['auth_user_id']
    })

    # First 25 Messages
    for idx in range(0, 25):
        requests.post(f'{config.url}message/send/v1', json={
            'token': member1['token'],
            'channel_id': channel_id.json()['channel_id'],
            'message': "Goodbye World"})
    # Next 50 Messages
    for idx in range(0, 50):
        requests.post(f'{config.url}message/send/v1', json={
            'token': owner['token'],
            'channel_id': channel_id.json()['channel_id'],
            'message': "Hello World"})
    # Next 50 Messages
    for idx in range(0, 50):
        requests.post(f'{config.url}message/send/v1', json={
            'token': member1['token'],
            'channel_id': channel_id.json()['channel_id'],
            'message': "Evening World"})

    channel_messages1 = requests.get(f'{config.url}channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_id.json()['channel_id'],
        'start': 0
    })

    channel_messages2 = requests.get(f'{config.url}channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_id.json()['channel_id'],
        'start': 50
    })

    channel_messages3 = requests.get(f'{config.url}channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_id.json()['channel_id'],
        'start': 100
    })

    assert channel_messages1.status_code == 200
    channel_messages1_info = channel_messages1.json()['messages']
    assert len(channel_messages1_info) == 50

    for idx in range(0, 50):
        assert channel_messages1_info[idx]['message_id'] == 125 - idx
        assert channel_messages1_info[idx]['u_id'] == member1['auth_user_id']
        assert channel_messages1_info[idx]['message'] == "Evening World"

    assert channel_messages1.json()['end'] == 50
    assert channel_messages1.json()['start'] == 0

    assert channel_messages2.status_code == 200
    channel_messages2_info = channel_messages2.json()['messages']
    assert len(channel_messages2_info) == 50

    for idx in range(0, 50):
        assert channel_messages2_info[idx]['message_id'] == 75 - idx
        assert channel_messages2_info[idx]['u_id'] == owner['auth_user_id']
        assert channel_messages2_info[idx]['message'] == "Hello World"

    assert channel_messages2.json()['end'] == 100
    assert channel_messages2.json()['start'] == 50

    assert channel_messages3.status_code == 200
    channel_messages3_info = channel_messages3.json()['messages']
    assert len(channel_messages3_info) == 25
    for idx in range(0, 25):
        assert channel_messages3_info[idx]['message_id'] == 25 - idx
        assert channel_messages3_info[idx]['u_id'] == member1['auth_user_id']
        assert channel_messages3_info[idx]['message'] == "Goodbye World"

    assert channel_messages3.json()['end'] == -1
    assert channel_messages3.json()['start'] == 100
