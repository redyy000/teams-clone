from email import message
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


def test_share_channel_success(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    message_id = message_response3.json()['message_id']
    message_response4 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_id,
        "message": "",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })

    assert message_response4.status_code == 200
    assert message_response4.json()['shared_message_id'] == 3

    message_id2 = dm_response.json()['message_id']

    message_response5 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_id2,
        "message": "",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })
    assert message_response5.status_code == 200
    assert message_response5.json()['shared_message_id'] == 4

    message_response6 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })
    assert message_response6.status_code == 200
    assert message_response6.json()['message_id'] == 5


def test_share_dm_long(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    share_response1 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_response3.json()['message_id'],
        "message": "AAAA" * 600,
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })
    assert share_response1.status_code == 400


def test_share_dm_success(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    message_id = message_response3.json()['message_id']
    share_response1 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_id,
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id1.json()['dm_id']
    })
    assert share_response1.status_code == 200
    message_id2 = dm_response.json()['message_id']

    share_response2 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_id2,
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id1.json()['dm_id']
    })
    assert share_response2.status_code == 200


def test_share_non_dm_member(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    # Member1 attempts to share to unjoined channel
    channel1 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    share_response1 = requests.post(f"{config.url}message/share/v1", json={
        "token": member1['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": channel1.json()['channel_id'],
        "dm_id": -1
    })

    assert share_response1.status_code == 403

    # Member1 attemps to share to unjoined DM

    dm_id2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': []})
    share_response2 = requests.post(f"{config.url}message/share/v1", json={
        "token": member1['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id2.json()['dm_id']
    })

    assert share_response2.status_code == 403


def test_share_non_channel_member(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel1 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    # Owner owns channel
    # Member Joins

    requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id': channel1.json()['channel_id']
    })

    channel2 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "AKENA",
        "is_public": True
    })

    # Member attempts to share owner's message to channel2

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": member1['token'],
        "og_message_id": message_response3.json()['message_id'],
        "message": "",
        "channel_id": channel2.json()['channel_id'],
        "dm_id": -1
    })

    assert share_response.status_code == 403

    # Attempt to share unowned DM
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': []
    })

    share_response2 = requests.post(f"{config.url}message/share/v1", json={
        "token": member1['token'],
        "og_message_id": message_response3.json()['message_id'],
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id1.json()['dm_id']
    })

    assert share_response2.status_code == 403


def test_share_invalid_ids(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": 999,
        "dm_id": -1
    })
    assert share_response.status_code == 400

    share_response2 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": -1,
        "dm_id": 999
    })
    assert share_response2.status_code == 400


def test_share_neither_ids_minus_one(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": dm_id1.json()['dm_id']
    })
    assert share_response.status_code == 400


def test_share_invalid_message_id(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": dm_response.json()['message_id'] + 10,
        "message": "",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })
    assert share_response.status_code == 400


def test_invalid_message_length(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "LMAO" * 1000,
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })
    assert share_response.status_code == 400


def test_invalid_token(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2, u_id3]})

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    message_response3 = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every ring has no maidens'
    })

    message_id = message_response3.json()['message_id']
    share_response1 = requests.post(f"{config.url}message/share/v1", json={
        "token": "THISAINTATOKEN",
        "og_message_id": message_id,
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id1.json()['dm_id']
    })
    assert share_response1.status_code == 403


def test_share_not_joined(setup_users):
    owner = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    u_id2 = user2['auth_user_id']
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [u_id2]})

    dm_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'message': "Hello World"})

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    share_response = requests.post(f"{config.url}message/share/v1", json={
        "token": user2['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })
    assert share_response.status_code == 403

    share_response2 = requests.post(f"{config.url}message/share/v1", json={
        "token": user3['token'],
        "og_message_id": dm_response.json()['message_id'],
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id1.json()['dm_id']
    })
    assert share_response2.status_code == 403
