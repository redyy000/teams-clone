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


def test_user_stats_channels(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # 1/3 Channels,

    # Create Channels

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "1",
        "is_public": True
    })

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "2",
        "is_public": True
    })

    user_stat_response1 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response1.status_code == 200
    assert len(user_stat_response1.json()[
               'user_stats']['channels_joined']) == 3
    assert user_stat_response1.json(
    )['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert user_stat_response1.json(
    )['user_stats']['channels_joined'][1]['num_channels_joined'] == 1
    assert user_stat_response1.json(
    )['user_stats']['channels_joined'][2]['num_channels_joined'] == 2

    # Join/Invite into channel

    channel3 = requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "3",
        "is_public": True
    }).json()

    channel4 = requests.post(f"{config.url}channels/create/v2", json={
        "token": member2['token'],
        "name": "4",
        "is_public": True
    }).json()

    # Invite
    invite = requests.post(f'{config.url}channel/invite/v2', json={
        'token': member1['token'],
        'channel_id': channel3['channel_id'],
        'u_id': owner['auth_user_id']
    })
    assert invite.status_code == 200

    user_stat_response9 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response9.status_code == 200
    assert len(user_stat_response9.json()[
               'user_stats']['channels_joined']) == 4
    assert user_stat_response9.json(
    )['user_stats']['channels_joined'][3]['num_channels_joined'] == 3

    # Join
    requests.post(f'{config.url}channel/join/v2', json={
        'token': owner['token'],
        'channel_id': channel4['channel_id']
    })

    user_stat_response2 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response2.status_code == 200
    assert len(user_stat_response2.json()[
               'user_stats']['channels_joined']) == 5
    assert user_stat_response2.json(
    )['user_stats']['channels_joined'][3]['num_channels_joined'] == 3
    assert user_stat_response2.json(
    )['user_stats']['channels_joined'][4]['num_channels_joined'] == 4

    # Leave
    leave = requests.post(f"{config.url}channel/leave/v1", json={
        'token': owner['token'],
        'channel_id': channel3['channel_id']})

    assert leave.status_code == 200

    user_stat_response3 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response3.status_code == 200
    assert len(user_stat_response3.json()[
               'user_stats']['channels_joined']) == 6
    assert user_stat_response3.json(
    )['user_stats']['channels_joined'][5]['num_channels_joined'] == 3


def test_user_stats_dms(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]
    # DM create

    dm1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    dm2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member2['auth_user_id']]
    })

    # DM leave
    user_stat_response1 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response1.status_code == 200
    assert len(user_stat_response1.json()['user_stats']['dms_joined']) == 3
    assert user_stat_response1.json(
    )['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert user_stat_response1.json(
    )['user_stats']['dms_joined'][1]['num_dms_joined'] == 1
    assert user_stat_response1.json(
    )['user_stats']['dms_joined'][2]['num_dms_joined'] == 2

    requests.post(f'{config.url}dm/leave/v1', json={
        'token': owner['token'],
        'dm_id': dm1.json()['dm_id']
    })

    user_stat_response2 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response2.status_code == 200
    assert len(user_stat_response2.json()['user_stats']['dms_joined']) == 4
    assert user_stat_response2.json(
    )['user_stats']['dms_joined'][3]['num_dms_joined'] == 1

    # DM Remove

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm2.json()['dm_id']
    })

    user_stat_response3 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response3.status_code == 200
    assert len(user_stat_response3.json()['user_stats']['dms_joined']) == 5
    assert user_stat_response3.json(
    )['user_stats']['dms_joined'][4]['num_dms_joined'] == 0


def test_user_stats_messages(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    # Channel, DM

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    }).json()

    channel = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "1",
        "is_public": True
    }).json()

    # Send Message
    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel['channel_id'],
        "message": 'Every soul has its dark'
    })

    # Send Dm Messages
    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': "Hello World"})

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': "Goodbye world"})

    user_stat_response1 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response1.status_code == 200
    assert len(user_stat_response1.json()['user_stats']['messages_sent']) == 4
    assert user_stat_response1.json(
    )['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert user_stat_response1.json(
    )['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert user_stat_response1.json(
    )['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert user_stat_response1.json(
    )['user_stats']['messages_sent'][3]['num_messages_sent'] == 3

    # Remove Message

    requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
    })

    user_stat_response2 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response2.status_code == 200
    assert len(user_stat_response2.json()['user_stats']['messages_sent']) == 4

    # Remove DM
    # No change to msgs sent

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm['dm_id']
    })

    user_stat_response3 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response3.status_code == 200
    assert len(user_stat_response3.json()['user_stats']['messages_sent']) == 4


def test_user_stats_involvement(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # 1/2 Dms
    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    }).json()

    dm2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': member2['token'],
        'u_ids': [member1['auth_user_id']]
    }).json()

    # 1/3 Chans
    channel = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "1",
        "is_public": True
    }).json()

    channel2 = requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "2",
        "is_public": True
    }).json()

    requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "3",
        "is_public": True
    }).json()

    # 1/3 messages
    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel['channel_id'],
        "message": 'Every soul has its dark'
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": member1['token'],
        "channel_id": channel2['channel_id'],
        "message": 'Every soul has its dark'
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": member1['token'],
        "channel_id": channel2['channel_id'],
        "message": 'Every soul has its dark'
    })

    # Send Dm Messages
    # 1/2
    owner_dm_msg = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm['dm_id'],
        'message': "Hello World"})

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm2['dm_id'],
        'message': "agwwgw World"})

    # Test message remove/ dm remove does not change msgs sent.
    # But it would change total messages..

    user_stat_response1 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response1.status_code == 200
    assert user_stat_response1.json(
    )['user_stats']['involvement_rate'] == float(4)/float(10)

    # Remove DM messages

    requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": owner_dm_msg.json()['message_id'],
    })

    user_stat_response2 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response2.status_code == 200
    assert user_stat_response2.json(
    )['user_stats']['involvement_rate'] == float(4)/float(9)

    # Remove DM completely

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm['dm_id']
    })

    user_stat_response3 = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response3.status_code == 200
    assert user_stat_response3.json(
    )['user_stats']['involvement_rate'] == float(3)/float(8)
