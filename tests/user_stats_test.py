import pytest
import requests
from datetime import timezone
import datetime
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

    user1_info = (response1.json())
    user2_info = (response2.json())
    user3_info = (response3.json())
    userlist.append(user1_info)
    userlist.append(user2_info)
    userlist.append(user3_info)
    return userlist


def test_user_stats_success(setup_users):
    owner = setup_users[0]
    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response.status_code == 200


def test_user_stats_invalid_token(setup_users):
    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': 'wehjgowheoighjwioeghoiwhegio'
    })

    assert user_stat_response.status_code == 403


'''
def test_user_stats_functionality(setup_users):

    
    
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # 1/3 Channels,

    # 1/2 DMs

    channel1 = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "1",
        "is_public": True
    })

    requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "2",
        "is_public": True
    })

    requests.post(f"{config.url}channels/create/v2", json={
        "token": member2['token'],
        "name": "3",
        "is_public": False
    })

    # Send a message
    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel1.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    dm1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    dm2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': member1['token'],
        'u_ids': []
    })

    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response.status_code == 200

    stats = user_stat_response.json()['user_stats']

    # Approximation
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    time_stamp = int(utc_time.timestamp())

    assert stats['channels_joined'] == [{1, time_stamp}]
    assert stats['dms_joined'] == [{1, time_stamp}]
    assert stats['messages_sent'] == [{1, time_stamp}]
    assert stats['involvement_rate'] == 0.5

'''
# More user stats tests with extra options.......


# Test with sendlater, standups
