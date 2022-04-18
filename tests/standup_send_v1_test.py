import pytest
import threading
import json
import requests
import time
from src import config
from src import auth
from src import channels
from src import channel
from src import other
from src import standup
from src import error
from datetime import timezone
import datetime


def long_message():
    return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


@pytest.fixture
def init():
    requests.delete(f'{config.url}clear/v1')
    user1 = requests.post(f'{config.url}auth/register/v2', json={'email': "dlin@gmail.com",
                                                                 'password': "password",
                                                                 'name_first': "daniel",
                                                                 'name_last': "lin"}).json()
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 1",
        'is_public': True
    }).json()
    channel2 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 2",
        'is_public': True
    }).json()
    channel3 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 3",
        'is_public': True
    }).json()
    return {"user": user1['token'], "channel1": channel1["channel_id"], "channel2": channel2["channel_id"], 'channel3': channel3["channel_id"]}


def test_standup_send_invalid_channel(init):
    # test channel id invalid --> input error
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": "invalid channel",
        "message": "hello world",
    })
    assert response.status_code == 400
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": 200,
        "message": "hello world",
    })
    assert response.status_code == 400


def test_standup_send_message_invalid(init):
    # test message length > 1000 --> input error
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": long_message(),
    })
    assert response.status_code == 400
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": 200,
    })
    assert response.status_code == 400
    time.sleep(2)


def test_standup_send_standup_invalid(init):
    # test message length > 1000 --> input error
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    time.sleep(2)
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "hello world",
    })
    assert response.status_code == 400


def test_standup_send_user_invalid(init):
    # test user not in channel --> access error
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movingotn@gmail.com",
                                                                 'password': "newpassword",
                                                                 'name_first': "Max",
                                                                 'name_last': "Ovington"}).json()
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": user2["token"],
        "channel_id": init["channel1"],
        "message": "hello world",
    })
    assert response.status_code == 403
    time.sleep(2)


def test_standup_send_token_invalid(init):
    # test message length > 1000 --> input error
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": "invalid token",
        "channel_id": init["channel1"],
        "message": "hello world",
    })
    assert response.status_code == 403
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": 200,
        "channel_id": init["channel1"],
        "message": "hello world",
    })
    assert response.status_code == 403


def test_standup_send_success(init):
    # note set thread time < 3 seconds
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    current_time = utc_time.timestamp() + 2
    #current_time = utc_time.timestamp() + 2

    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 1",
    })
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 2",
    })
    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 3",
    })
    assert response.status_code == 200
    time.sleep(2)

    # Check for notifications

    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': init["user"],
        'channel_id': init["channel1"],
        'start': 0
    })
    assert response.status_code == 200
    messages = response.json()["messages"]

    #assert len(messages) == 1
    assert messages[0]['message_id'] == 1
    assert messages[0]['u_id'] == 1
    assert messages[0]['message'] == "daniellin: Message 1\ndaniellin: Message 2\ndaniellin: Message 3"

    # margin of error less than half a second
    assert messages[0]['time_sent'] - current_time < 0.5


def test_standup_send_success_removed_user(init):
    # tests that a removed user (i.e. doesn't exist) does not appear in the buffer

    #current_time = utc_time.timestamp() + 2
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movingotn@gmail.com",
                                                                 'password': "newpassword",
                                                                 'name_first': "Max",
                                                                 'name_last': "Ovington"}).json()
    requests.post(f"{config.url}channel/invite/v2", json={'token': init["user"],
                                                          'channel_id': init["channel1"],
                                                          'u_id': user2["auth_user_id"]})

    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    assert response.status_code == 200
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 1",
    })
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 2",
    })

    response = requests.post(f'{config.url}standup/send/v1', json={
        "token": user2["token"],
        "channel_id": init["channel1"],
        "message": "Message 3",
    })
    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': init["user"],
        'u_id': user2["auth_user_id"],
    })
    assert response.status_code == 200
    time.sleep(2)
    response = requests.get(f'{config.url}standup/active/v1', params={
        "token": init["user"],
        "channel_id": init["channel1"],
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': init["user"],
        'channel_id': init["channel1"],
        'start': 0
    })
    assert response.status_code == 200
    messages = response.json()["messages"]

    assert messages[0]['message_id'] == 1
    assert messages[0]['u_id'] == 1
    assert messages[0]['message'] == "daniellin: Message 1\ndaniellin: Message 2"


def test_standup_send_success_no_user_admin_remove(init):
    # tests when a user is removed they don't appear in the buffer
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movingotn@gmail.com",
                                                                 'password': "newpassword",
                                                                 'name_first': "Max",
                                                                 'name_last': "Ovington"}).json()
    requests.post(f"{config.url}channel/invite/v2", json={'token': init["user"],
                                                          'channel_id': init["channel1"],
                                                          'u_id': user2["auth_user_id"]})
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": user2["token"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 1",
    })
    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': init["user"],
        'u_id': user2["auth_user_id"],
    })
    time.sleep(2)
    response = requests.get(f'{config.url}standup/active/v1', params={
        "token": init["user"],
        "channel_id": init["channel1"],
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': init["user"],
        'channel_id': init["channel1"],
        'start': 0
    })
    assert response.status_code == 200
    assert response.json()["messages"] == []


def test_standup_send_success_no_user_channel_leave_2(init):
    # tests when the standup user is removed by admin nothing happens
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movingotn@gmail.com",
                                                                 'password': "newpassword",
                                                                 'name_first': "Max",
                                                                 'name_last': "Ovington"}).json()
    requests.post(f"{config.url}channel/invite/v2", json={'token': init["user"],
                                                          'channel_id': init["channel1"],
                                                          'u_id': user2["auth_user_id"]})
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": user2["auth_user_id"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 1",
    })
    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': init["user"],
        'u_id': user2["auth_user_id"],
    })
    time.sleep(2)
    response = requests.get(f'{config.url}standup/active/v1', params={
        "token": init["user"],
        "channel_id": init["channel1"],
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
    response = requests.get(f'{config.url}channel/messages/v2', params={
        'token': init["user"],
        'channel_id': init["channel1"],
        'start': 0
    })
    assert response.status_code == 200
    assert response.json()["messages"] == []


def test_standup_send_success_no_user_channel_leave(init):
    # Test the user cannot be removed from the channel
    user3 = requests.post(f'{config.url}auth/register/v2', json={'email': "tslater@gmail.com",
                                                                 'password': "nnupassword",
                                                                 'name_first': "Tayla",
                                                                 'name_last': "Slater"}).json()
    requests.post(f"{config.url}channel/invite/v2", json={'token': init["user"],
                                                          'channel_id': init["channel1"],
                                                          'u_id': user3["auth_user_id"]})
    response = requests.post(f'{config.url}standup/start/v1', json={
        "token": user3["token"],
        "channel_id": init["channel1"],
        "length": 2,
    })
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    current_time = int(utc_time.timestamp() + 2)
    assert response.status_code == 200
    assert response.json() == {"time_finish": current_time}

    requests.post(f'{config.url}standup/send/v1', json={
        "token": init["user"],
        "channel_id": init["channel1"],
        "message": "Message 1",
    })
    response = requests.get(f'{config.url}standup/active/v1', params={
        "token": init["user"],
        "channel_id": init["channel1"],
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": True, "time_finish": current_time}
    response = requests.post(f"{config.url}channel/leave/v1", json={
        'token': user3["token"],
        'channel_id': init["channel1"],
    })
    assert response.status_code == 400
