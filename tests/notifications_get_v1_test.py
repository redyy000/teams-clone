import pytest
import requests
from src import config

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
def george_token():
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
    requests.delete(f"{config.url}/clear/v1")
    # should return an empty list
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert notifications.json() == {'notifications': []}


def test_notifications_get_one_notification(george_token, channel_id):
    requests.delete(f"{config.url}/clear/v1")
    requests.post(config.url + '/message/send/v2', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey"
    })
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert len(notifications.json()['notifications']) == 1


def test_notifications_get_correct_type(george_token, channel_id):
    requests.delete(f"{config.url}/clear/v1")

    requests.post(config.url + '/message/send/v2', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey"
    })
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    }).json()

    assert 'channel_id' in notifications['notifications'][0]
    assert 'dm_id' in notifications['notifications'][0]
    assert 'notification_message' in notifications['notifications'][0]


def test_notfications_get_multiple_tagged_with_1_valid_user(george_token, channel_id):
    requests.post(config.url + '/message/send/v2', json={
        'token': george_token,
        'channel_id': channel_id,
        'message': "Hi @georgemonkey and @randomname and @otherrandomname"
    })
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    })
    assert len(notifications.json()['notifications']) == 1


def test_notifications_get_at_most_20_returned(george_token, channel_id):
    for i in range(0, 30):
        requests.post(f'{config.url}/message/send/v2', json={
            'token': george_token,
            'channel_id': channel_id,
            'message': f"Test {i} message @georgemonkey"})
    notifications = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': george_token
    }).json()
    assert len(notifications['notifications']) == 20
