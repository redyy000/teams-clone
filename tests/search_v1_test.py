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


def test_search_success_case_channels(setup_users):
    owner = setup_users[0]
    user1 = setup_users[1]
    user2 = setup_users[2]

    # create channel, invite user 1 and send messages
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': "Public Channel",
        'is_public': True
    })
    assert channel1.status_code == 200

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': user1['auth_user_id']
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "TEST CHANNEL"
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "test channel"
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "testchannel"
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "channel test"
    })

    # Case insensitive
    search = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': 'Test CHANNEL'})

    assert search.status_code == 200

    messages_list = []
    for message in search.json()['messages']:
        messages_list.append(message['message'])

    assert 'TEST CHANNEL' in messages_list
    assert 'test channel' in messages_list
    assert len(messages_list) == 2


def test_search_success_case_dms(setup_users):
    owner = setup_users[0]
    user1 = setup_users[1]
    user2 = setup_users[2]

    # create dm, send messages
    new_dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [user1['auth_user_id'], user2['auth_user_id']]
    }).json()
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': new_dm['dm_id'],
        'message': "DM TEST"
    })
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': new_dm['dm_id'],
        'message': "dm test"
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': new_dm['dm_id'],
        'message': "dmtest"
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': new_dm['dm_id'],
        'message': "dm TEST"
    })

    search = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': 'Dm TeSt'})

    assert search.status_code == 200

    messages_list = []
    for message in search.json()['messages']:
        messages_list.append(message['message'])

    assert 'DM TEST' in messages_list
    assert 'dm test' in messages_list
    assert 'dm TEST' in messages_list
    assert len(messages_list) == 3


def test_search_success(setup_users):
    owner = setup_users[0]
    user1 = setup_users[1]
    user2 = setup_users[2]

    # create channel, invite user 1 and send messages
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': "Public Channel",
        'is_public': True
    })
    assert channel1.status_code == 200

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': user1['auth_user_id']
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "Test channel message first"
    })
    requests.post(f"{config.url}message/send/v1", json={
        "token": user1['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": "Test channel message second"
    })

    # create dm, send messages
    new_dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [user1['auth_user_id'], user2['auth_user_id']]
    }).json()
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': new_dm['dm_id'],
        'message': "Test dm message first"
    })
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': user2['token'],
        'dm_id': new_dm['dm_id'],
        'message': "Test dm message second"
    })

    search = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': 'first'})

    assert search.status_code == 200

    messages_list = []
    for message in search.json()['messages']:
        messages_list.append(message['message'])

    assert 'Test channel message first' in messages_list
    assert 'Test dm message first' in messages_list
    assert len(messages_list) == 2


def test_search_empty(setup_users):
    owner = setup_users[0]
    search = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'],  'query_str': 'searching messages...'})

    assert search.status_code == 200
    messages_list = []
    for message in search.json()['messages']:
        messages_list.append(message['message'])
    assert len(messages_list) == 0


def test_search_invalid_token():
    response_invalid = requests.get(f'{config.url}/search/v1', params={
        'token': 'invalid_token', 'query_str': 'searching messages...'})
    assert response_invalid.status_code == 403


def test_search_query_string_short(setup_users):
    owner = setup_users[0]
    response = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': ''})
    assert response.status_code == 400


def test_search_query_string_long(setup_users):
    owner = setup_users[0]
    response = requests.get(f'{config.url}/search/v1', params={
        'token': owner['token'], 'query_str': 200 * 'This is too long'})
    assert response.status_code == 400
