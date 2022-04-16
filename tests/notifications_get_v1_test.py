import pytest
import requests
from src import config
import datetime
import time


'''
    Tests for notifications_get_v1
    Parameters: token
    Return Type: notifications

    List of dictionaries, where each dictionary contains types { channel_id, dm_id, notification_message } where channel_id is the id of the channel that the event happened in, and is -1 if it is being sent to a DM. dm_id is the DM that the event happened in, and is -1 if it is being sent to a channel. Notification_message is a string of the following format for each trigger action:

        tagged: "{User's handle} tagged you in {channel/DM name}: {first 20 characters of the message}"
        reacted message: "{User's handle} reacted to your message in {channel/DM name}"
        added to a channel/DM: "{User's handle} added you to {channel/DM name}"
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


@pytest.fixture
def george_token():
    requests.delete(f"{config.url}/clear/v1")
    '''
    Creates test user named George Monkey, email george@gmail.com.
    '''
    post_george = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': 'monkey',
        'name_first': 'George',
        'name_last': 'Monkey',
    })
    george_data = post_george.json()
    return george_data['token']


@pytest.fixture
def channel_id(george_token):
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': george_token,
        'name': "Public Channel",
        'is_public': True
    }).json()
    return channel1['channel_id']


def test_notifications_get_invalid_token():
    requests.delete(f"{config.url}/clear/v1")
    response = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': 'invalid_token'
    })
    assert response.status_code == 403


def test_notifications_get_no_new_notifications(george_token):
    # should return an empty list
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert notifications.json() == {'notifications': []}


def test_notifications_get_one_notification(george_token):

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': george_token,
        'name': "Public Channel",
        'is_public': True
    }).json()['channel_id']

    send = requests.post(f'{config.url}/message/send/v1', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey"
    })

    assert send.status_code == 200
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert len(notifications.json()['notifications']) == 1


def test_notifications_get_correct_type(george_token):

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': george_token,
        'name': "Public Channel",
        'is_public': True
    }).json()['channel_id']

    send = requests.post(config.url + '/message/send/v1', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey"
    })

    assert send.status_code == 200

    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    }).json()

    assert 'channel_id' in notifications['notifications'][0]
    assert 'dm_id' in notifications['notifications'][0]
    assert 'notification_message' in notifications['notifications'][0]


def test_notfications_get_multiple_tagged_with_1_valid_user(george_token):

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': george_token,
        'name': "Public Channel",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + '/message/send/v1', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey and @randomname and @otherrandomname"
    })

    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })

    assert len(notifications.json()['notifications']) == 1
    note = notifications.json()['notifications']
    assert note[0]['notification_message'] == "georgemonkey tagged you in Public Channel: Hi @georgemonkey and"
    assert note[0]['dm_id'] == -1
    assert note[0]['channel_id'] == channel_id


def test_notifications_get_at_most_20_returned(george_token):

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': george_token,
        'name': "Public Channel",
        'is_public': True
    }).json()['channel_id']

    for i in range(0, 30):
        requests.post(f'{config.url}/message/send/v1', json={
            'token': george_token,
            'channel_id': channel_id,
            'message': "@georgemonkey1234567890"})
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert notifications.status_code == 200
    assert len(notifications.json()['notifications']) == 20

    for i in range(0, 20):
        note = notifications.json()['notifications']
        assert note[i][
            'notification_message'] == f"georgemonkey tagged you in Public Channel: @georgemonkey1234567"
        assert note[i]['dm_id'] == -1
        assert note[i]['channel_id'] == channel_id

        # DM Based Tests


def test_notifications_get_dm_invite(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    assert dm1.status_code == 200

    dm2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member2['auth_user_id']]
    })

    assert dm2.status_code == 200

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': member1['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0]['notification_message'] == 'daniellin added you to daniellin, richardxue, ryangodakanda'
    assert note[0]['dm_id'] == 1
    assert note[0]['channel_id'] == -1

    notification_member2 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': member2['token']
    })

    assert notification_member2.status_code == 200
    note2 = notification_member2.json()['notifications']

    assert len(note2) == 2

    # Inverse order, most recent to last

    assert note2[0]['notification_message'] == 'daniellin added you to daniellin, ryangodakanda'
    assert note2[0]['dm_id'] == dm2.json()['dm_id']
    assert note2[0]['channel_id'] == -1
    assert note2[1]['notification_message'] == 'daniellin added you to daniellin, richardxue, ryangodakanda'
    assert note2[1]['dm_id'] == dm1.json()['dm_id']
    assert note2[1]['channel_id'] == -1


# Channel based tests


def test_notifications_get_channel_invite(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    channel1 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel1.json()['channel_id'],
        'u_id': member1['auth_user_id']
    })

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': member1['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0]['notification_message'] == 'daniellin added you to general'
    assert note[0]['dm_id'] == -1
    assert note[0]['channel_id'] == 1


def test_notifications_react_channel(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id':  channel_response.json()['channel_id']
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    react_response = requests.post(f"{config.url}message/react/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        "react_id": 1
    })

    assert react_response.status_code == 200

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0][
        'notification_message'] == 'richardxue reacted to your message in general'
    assert note[0]['dm_id'] == -1
    assert note[0]['channel_id'] == 1


def test_notifications_react_dms(setup_users):

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

    react_response = requests.post(f"{config.url}message/react/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        "react_id": 1
    })

    assert react_response.status_code == 200

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0][
        'notification_message'] == 'richardxue reacted to your message in daniellin, richardxue'
    assert note[0]['dm_id'] == 1
    assert note[0]['channel_id'] == -1


def test_notifications_sendlater_channels(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response1 = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": '@daniellin bruh',
        "time_sent": time_now + 1
    })

    assert message_response1.status_code == 200
    time.sleep(1.5)

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0][
        'notification_message'] == 'daniellin tagged you in general: @daniellin bruh'
    assert note[0]['dm_id'] == -1
    assert note[0]['channel_id'] == 1


def test_notifications_sendlater_dms(setup_users):

    owner = setup_users[0]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': []
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response1 = requests.post(f"{config.url}message/sendlaterdm/v1", json={
        "token": owner['token'],
        "dm_id": dm.json()['dm_id'],
        "message": '@daniellin bruh',
        "time_sent": time_now + 1
    })

    assert message_response1.status_code == 200
    time.sleep(1.5)

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 1
    assert note[0][
        'notification_message'] == 'daniellin tagged you in daniellin: @daniellin bruh'
    assert note[0]['dm_id'] == 1
    assert note[0]['channel_id'] == -1


def test_notifications_share_channels(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": '@daniellin bruh'
    })

    requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_response.json()['message_id'],
        "message": "wow",
        "channel_id": channel_response.json()['channel_id'],
        "dm_id": -1
    })

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 2
    assert note[0][
        'notification_message'] == 'daniellin tagged you in general: @daniellin bruh wow'
    assert note[0]['dm_id'] == -1
    assert note[0]['channel_id'] == 1
    assert note[1][
        'notification_message'] == 'daniellin tagged you in general: @daniellin bruh'
    assert note[1]['dm_id'] == -1
    assert note[1]['channel_id'] == 1


def test_notifications_share_dms(setup_users):

    owner = setup_users[0]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': []
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': '@daniellin bruh'})

    message_id = message_response.json()['message_id']

    share_response1 = requests.post(f"{config.url}message/share/v1", json={
        "token": owner['token'],
        "og_message_id": message_id,
        "message": "wow",
        "channel_id": -1,
        "dm_id": dm.json()['dm_id']
    })
    assert share_response1.status_code == 200

    notification_member1 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member1.status_code == 200
    note = notification_member1.json()['notifications']
    assert len(note) == 2
    assert note[0][
        'notification_message'] == 'daniellin tagged you in daniellin: @daniellin bruh wow'
    assert note[0]['dm_id'] == 1
    assert note[0]['channel_id'] == -1
    assert note[1][
        'notification_message'] == 'daniellin tagged you in daniellin: @daniellin bruh'
    assert note[1]['dm_id'] == 1
    assert note[1]['channel_id'] == -1
