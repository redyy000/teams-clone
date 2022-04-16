
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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': 99999,
        'message': "Hello World"})

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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': -1,
        'message': "Hello World"})

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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': {}})
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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': user3['token'],
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World"})

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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': "THISAINTATOKEN!!",
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World"})
    assert response.status_code == 403


def test_messages_senddm_non_member(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]

    token_id1 = user1['token']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': []})

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "@richardxue"})

    assert response.status_code == 200

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': user2['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 0


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

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World"})

    assert response.status_code == 200

    response2 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'start': 0
    }).json()

    message_list = response2['messages']

    assert message_list[0]['u_id'] == user1['auth_user_id']
    assert message_list[0]['message'] == "Hello World"

    assert response2['end'] == -1


def test_messages_senddm_multiple_dms(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    dm_id_2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2, u_id3]})

    response1 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_1.json()['dm_id'],
        'message': "Hello World"})

    assert response1.status_code == 200

    response2 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': token_id1,
        'dm_id': dm_id_2.json()['dm_id'],
        'message': "Goodbye World"})

    assert response2.status_code == 200
