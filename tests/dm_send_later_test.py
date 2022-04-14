import pytest
import requests
from src import config
import datetime


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

    user1_info = (response1.json())
    user2_info = (response2.json())
    user3_info = (response3.json())
    userlist.append(user1_info)
    userlist.append(user2_info)
    userlist.append(user3_info)
    return userlist


def test_messages_senddm_invalid_dm_id(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': token_id1,
        'dm_id': 99999,
        'message': "Hello World",
        'time_sent': time_now + 1
    })

    assert response.status_code == 400


def test_messages_senddm_negative_dm_id(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': token_id1,
        'dm_id': -1,
        'message': "Hello World",
        'time_sent': time_now + 1
    })

    assert response.status_code == 400


def test_messages_senddm_invalid_message_length(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']
    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': '',
        'time_sent': time_now + 1
    })
    assert response.status_code == 400


def test_messages_senddm_invalid_auth_user(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': user3['token'],
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World",
        'time_sent': time_now + 1
    })

    assert response.status_code == 403


def test_messages_senddm_invalid_token(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': "THISAINTATOKEN!!",
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World",
        'time_sent': time_now + 1
    })
    assert response.status_code == 403


def test_messages_senddm_invalid_time(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World",
        'time_sent': time_now - 1
    })

    assert response.status_code == 400


# def test_dm_removed(setup_users):
#     user1 = setup_users[0]
#     user2 = setup_users[1]
#     user3 = setup_users[2]

#     token_id1 = user1['token']
#     u_id2 = user2['auth_user_id']
#     u_id3 = user3['auth_user_id']

#     dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
#         'token': token_id1,
#         'u_ids': [u_id2, u_id3]})

#     time_now = int(datetime.datetime.now().timestamp())
#     response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
#         'token': token_id1,
#         'dm_id': dm_id_1.json()['dm_id'],
#         'message': "Hello World",
#         'time_sent': time_now + 20
#     })

#     requests.delete(f"{config.url}/dm/remove/v1", json={
#         'token': token_id1,
#         'dm_id': dm_id_1.json()['dm_id']
#     })

#     assert response.json() == {}


def test_messages_senddm_success(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    time_now = int(datetime.datetime.now().timestamp())
    response = requests.post(f'{config.url}message/sendlaterdm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World",
        'time_sent': time_now + 2
    })

    assert response.status_code == 200
