import pytest
import requests
from src import config

'''
    Tests for search_v1
    Parameters: token, query_str
    Return Type: Messages
    Input Error: length of query_str is <1 or > 1000 characters
    
    Other errors:
        Access Error: invalid user ID/token
'''


@pytest.fixture
def setup_users():
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


# Admin creates a public channel, invites user 1, messages are sent:
@pytest.fixture
def setup_channel(setup_users):
    owner = setup_users[0]
    user1 = setup_users[1]
    channel = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': "Public",
        'is_public': True
    }).json()
    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user1['auth_user_id']
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel['channel_id'],
        "message": "Test channel message first"
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "message": "Test channel message second"
    })


# Admin creates a dm with users 1 and 2, sends some messages
@pytest.fixture
def setup_dm(setup_users):
    owner = setup_users[0]
    user1 = setup_users[1]
    user2 = setup_users[2]
    new_dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [user1['auth_user_id'], user2['auth_user_id']]
    }).json()
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': new_dm['dm_id'],
        'message': "Test dm message first "})
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': new_dm['dm_id'],
        'message': "Test dm message second"
    })


def test_search_success(setup_channel, setup_dm, setup_users):
    requests.delete(f"{config.url}/clear/v1")
    owner = setup_users[0]
    result = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': 'first'}).json()

    messages_list = []
    for message in result['messages']:
        messages_list.append(message['message'])

    assert 'Test channel message first' in messages_list
    assert 'Test dm message first' in messages_list
    assert len(messages_list) == 2


def test_invalid_token_dm(setup_dm):
    requests.delete(f"{config.url}/clear/v1")
    response = requests.get(config.url + '/search/v1', params={
        'token': 'invalid_token', 'query_str': 'searching messages...'})
    assert response.status_code == 403


def test_query_string_short(setup_dm, setup_users):
    requests.delete(f"{config.url}/clear/v1")
    owner = setup_users[0]
    response = requests.get(config.url + '/search/v1', params={
        'token': owner['token'], 'query_str': ''})
    assert response.status_code == 400


def test_query_string_long(setup_users):
    requests.delete(f"{config.url}/clear/v1")
    owner = setup_users[0]
    response = requests.get(config.url + '/search/v1', params={
        'token': owner['token'], 'query_str': 1001 * 'A'})
    assert response.status_code == 400
