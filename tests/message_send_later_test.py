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

    time_now = int(datetime.datetime.now().timestamp())
    message_response1 = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark',
        "time_sent": time_now + datetime.timedelta(seconds=10)
    })

    assert message_response1.status_code == 200


def test_message_send_invalid_token(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": 'hwgowehgiowehgoihwoiehg',
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark',
        "time_sent": time_now + datetime.timedelta(seconds=10)
    })

    assert message_response.status_code == 403


def test_message_send_invalid_channel_id(setup_users):

    owner = setup_users[0]

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": owner['token'],
        "channel_id": 999999999999,
        "message": 'Every soul has its dark',
        "time_sent": time_now + datetime.timedelta(seconds=10)
    })

    assert message_response.status_code == 400


def test_message_send_message_length_short(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": '',
        "time_sent": time_now + datetime.timedelta(seconds=10)
    })

    assert message_response.status_code == 400


def test_message_send_message_length_long(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    time_now = int(datetime.datetime.now().timestamp())
    message_response = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark' * 250,
        "time_sent": time_now + datetime.timedelta(seconds=10)
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

    time_now = int(datetime.datetime.now().timestamp())
    message_response = requests.post(f"{config.url}message/sendlater/v1", json={
        "token": member1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark',
        "time_sent": time_now + datetime.timedelta(seconds=10)
    })

    assert message_response.status_code == 403


def test_message_send_invalid_time(setup_users):
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
        "message": 'Every soul has its dark',
        "time_sent": time_now - datetime.timedelta(seconds=10)
    })

    assert message_response1.status_code == 400
