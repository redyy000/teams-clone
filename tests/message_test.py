import pytest
from src import config
import requests
import json
'''
InputError when any of:
    dm_id does not refer to a valid DM
    length of message is less than 1 or over 1000 characters

AccessError when:

    dm_id is valid and the authorised user is not a member of the DM
'''


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

    user1_info = json.loads(response1.json())
    user2_info = json.loads(response2.json())
    user3_info = json.load(response3.json())
    userlist.extend(user1_info, user2_info, user3_info)
    return userlist


def invalid_dm_id_test(setup_users):
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


def negative_dm_id_test(setup_users):
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


def invalid_message_length_test(setup_users):
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
        'dm_id': dm_id_1,
        'message': "{}"})
    assert response.status_code == 400


def invalid_auth_user_test(setup_users):
    user1 = setup_users[0]
    user2 = setup_users[1]
    user3 = setup_users[2]

    token_id1 = user1['token']
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    dm_id_1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': token_id1,
        'u_ids': [u_id2]})

    response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': user3['token'],
        'dm_id': dm_id_1,
        'message': "Hello World"})

    assert response.status_code == 403


def invalid_token_test(setup_users):
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
        'dm_id': dm_id_1,
        'message': "Hello World"})
    assert response.status_code == 403


def success_test(setup_users):
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
        'dm_id': dm_id_1,
        'message': "Hello World"})

    assert response.status_code == 200

    response2 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': token_id1,
        'dm_id': dm_id_1,
        'start': 0
    }).json()

    assert response2['end'] == -1
    assert response2['messages'][0] is "Hello World"
