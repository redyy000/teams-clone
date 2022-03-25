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


def test_message_send_multiple_users_in_channel(setup_users):
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
    user2_message = requests.post(f"{config.url}message/send/v1", json={
        "token": setup_users[2]['token'],
        "channel_id": channel_id,
        "message": 'Welcome to the jungle.'
    })
    assert user2_message.status_code == 200
    message_id1 = user2_message.json()['message_id']

    user1_message = requests.post(f"{config.url}message/send/v1", json={
        "token": setup_users[1]['token'],
        "channel_id": channel_id,
        "message": "We've got fun and games"
    })
    assert user1_message.status_code == 200

    message_id2 = user1_message.json()['message_id']

    # assert message_id2 == 2

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel_id,
        'start': 0
    })

    message_list = messages_response.json()['messages']
    for message_dict in message_list:
        if message_dict['message'] == 'Welcome to the jungle.':
            assert message_id1 == message_dict['message_id']
        if message_dict['message'] == "We've got fun and games":
            assert message_id2 == message_dict['message_id']


def test_message_send_multiple_users_in_dm(setup_users):
    # create dm
    owner = setup_users[0]
    user1 = setup_users[1]
    user2 = setup_users[2]

    dm_response = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [user1['auth_user_id'], user2['auth_user_id']]
    })
    assert dm_response.status_code == 200
    dm_id = dm_response.json()['dm_id']

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': owner['token'],
        'dm_id': dm_response.json()['dm_id']
    })
    dm_id = dm_response.json()['dm_id']

    # send multiple dms
    dm1 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm_id,
        'message': "Billy Jean is"
    })
    assert dm1.status_code == 200
    message_id1 = dm1.json()['message_id']

    dm2 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id,
        'message': "not my lover"
    })
    assert dm2.status_code == 200
    message_id2 = dm2.json()['message_id']

    dm3 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': dm_id,
        'message': "She's just a girl who claims that I am the one"
    })
    assert dm3.status_code == 200
    message_id3 = dm3.json()['message_id']

    # test responses
    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': owner['token'],
        'dm_id': dm_id,
        'start': 0
    })
    assert dm_messages.status_code == 200

    message_list = dm_messages.json()['messages']
    for dm_dict in message_list:
        if dm_dict['message'] == 'Billy Jean is':
            assert message_id1 == dm_dict['message_id']
        if dm_dict['message'] == "not my lover":
            assert message_id2 == dm_dict['message_id']
        if dm_dict['message'] == "She's just a girl who claims that I am the one":
            assert message_id3 == dm_dict['message_id']
