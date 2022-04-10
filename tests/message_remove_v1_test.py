import pytest
import requests
from src import config

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


def test_message_remove_success(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 200


def test_message_remove_invalid_token(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": 'eifghwoireghowiehgo',
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 403


def test_message_remove_invalid_message_id(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": 999999,
    })

    assert remove_response.status_code == 400


def test_message_remove_non_poster_non_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 403


def test_message_remove_non_global_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 403


def test_message_remove_dms(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    message_response1 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    message_response2 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'wogeihowighowehgoiwhoeighwoegowiheoig'})

    message_response3 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': member2['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'wogeih'})

    remove_response1 = requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": message_response2.json()['message_id'],
    })

    remove_response2 = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member1['token'],
        "message_id": message_response1.json()['message_id'],
    })

    remove_response3 = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member2['token'],
        "message_id": message_response3.json()['message_id'],
    })

    assert remove_response1.status_code == 200
    assert remove_response2.status_code == 200
    assert remove_response3.status_code == 200


def test_message_remove_dms_non_member(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'test message'})

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member2['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 403

# Non-sender but member of dm attempts to remove another
# Person's message


def test_message_remove_dms_non_sender(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 403


def test_message_remove_global_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f'{config.url}message/send/v1', json={
        'token': member1['token'],
        'channel_id': channel_response.json()['channel_id'],
        'message': 'bruh '})
    assert message_response.status_code == 200

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': owner['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    remove_response = requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
    })

    assert remove_response.status_code == 200

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    assert len(messages_response.json()['messages']) == 0
    assert messages_response.status_code == 200
