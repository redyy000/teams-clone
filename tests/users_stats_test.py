import pytest
import requests
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


def test_users_stats_success(setup_users):
    owner = setup_users[0]
    users_stats_response = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token'],
    })

    assert users_stats_response.status_code == 200


def test_users_stats_invalid_token(setup_users):
    users_stats_response = requests.get(f'{config.url}/users/stats/v1', params={
        'token': 'wehjgowheoighjwioeghoiwhegio'
    })

    assert users_stats_response.status_code == 403


def test_users_stats_channels(setup_users):
    owner = setup_users[0]
    # Add channels
    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    users_stats_response1 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response1.status_code == 200

    stats1 = users_stats_response1.json()
    assert len(stats1['workspace_stats']['channels_exist']) == 2
    assert stats1['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats1['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1

    requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "gengeojeojl",
        "is_public": True
    })

    users_stats_response2 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response2.status_code == 200

    stats2 = users_stats_response2.json()
    assert len(stats2['workspace_stats']['channels_exist']) == 3
    assert stats2['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats2['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1
    assert stats2['workspace_stats']['channels_exist'][2]['num_channels_exist'] == 2

    # Test channel join, invite.


def test_users_stats_dms(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]
    # Add Dms
    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    users_stats_response1 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response1.status_code == 200
    stats1 = users_stats_response1.json()
    assert len(stats1['workspace_stats']['dms_exist']) == 2
    assert stats1['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats1['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1

    requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    users_stats_response2 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response2.status_code == 200
    stats2 = users_stats_response2.json()
    assert len(stats2['workspace_stats']['dms_exist']) == 3
    assert stats2['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats2['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert stats2['workspace_stats']['dms_exist'][2]['num_dms_exist'] == 2

    # Remove Dms

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    users_stats_response3 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response3.status_code == 200
    stats3 = users_stats_response3.json()
    assert len(stats3['workspace_stats']['dms_exist']) == 4
    assert stats3['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats3['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert stats3['workspace_stats']['dms_exist'][2]['num_dms_exist'] == 2
    assert stats3['workspace_stats']['dms_exist'][3]['num_dms_exist'] == 1


def test_users_stats_utilization(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    # Ban Users

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    channel_info = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    })
    # Make users join channels and dms

    requests.post(f'{config.url}channel/join/v2', json={
        'token': setup_users[1]['token'],
        'channel_id': channel_info.json()['channel_id']
    })

    users_stats_response1 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response1.status_code == 200
    stats1 = users_stats_response1.json()
    assert stats1['workspace_stats']['utilization_rate'] == float(2)/float(3)

    # Channel leave and DM remove

    requests.post(f"{config.url}channel/leave/v1", json={
        'token': member1['token'],
        'channel_id': channel_info.json()['channel_id']
    })

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    users_stats_response2 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response2.status_code == 200
    stats2 = users_stats_response2.json()
    assert stats2['workspace_stats']['utilization_rate'] == float(1)/float(3)

    # Test Admin Remove

    requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    users_stats_response3 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response3.status_code == 200
    stats3 = users_stats_response3.json()
    assert stats3['workspace_stats']['utilization_rate'] == float(1)/float(2)

    # Removing someone already in?

    temp3 = requests.post(f'{config.url}auth/register/v2', json={'email': "gegjon@gmail.com",
                                                                 'password': "password",
                                                                 'name_first': "ryan",
                                                                 'name_last': "godakanda"}).json()

    requests.post(f'{config.url}channel/join/v2', json={
        'token': temp3['token'],
        'channel_id': channel_info.json()['channel_id']
    })

    users_stats_response4 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response4.status_code == 200
    stats4 = users_stats_response4.json()
    assert stats4['workspace_stats']['utilization_rate'] == float(2)/float(3)

    requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': temp3['auth_user_id'],
    })

    users_stats_response5 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response5.status_code == 200
    stats5 = users_stats_response5.json()
    assert stats5['workspace_stats']['utilization_rate'] == float(1)/float(2)


def test_users_stats_messages(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm_info = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id']]
    })

    channel_info = requests.post(f'{config.url}channels/create/v2', json={
        'token': setup_users[0]['token'],
        'name': "Public",
        'is_public': True
    })

    # Send messages

    channel_message = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_info.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    # Send dm messages

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm_info.json()['dm_id'],
        'message': "Hello World"
    })

    users_stats_response1 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response1.status_code == 200
    stats1 = users_stats_response1.json()
    assert len(stats1['workspace_stats']['messages_exist']) == 3
    assert stats1['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats1['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats1['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2

    # Remove dm

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm_info.json()['dm_id'],
        'message': "Htrojpojepjpe"
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm_info.json()['dm_id'],
        'message': "eeee"
    })

    requests.delete(f"{config.url}/dm/remove/v1", json={
        'token': owner['token'],
        'dm_id': dm_info.json()['dm_id']
    })

    users_stats_response2 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response2.status_code == 200
    stats2 = users_stats_response2.json()
    assert len(stats2['workspace_stats']['messages_exist']) == 6
    assert stats2['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats2['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats2['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2
    assert stats2['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 3
    assert stats2['workspace_stats']['messages_exist'][4]['num_messages_exist'] == 4
    assert stats2['workspace_stats']['messages_exist'][5]['num_messages_exist'] == 1

    # Remove channel messages

    requests.delete(f"{config.url}message/remove/v1", json={
        "token": owner['token'],
        "message_id": channel_message.json()['message_id'],
    })

    users_stats_response3 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response3.status_code == 200
    stats3 = users_stats_response3.json()
    assert len(stats3['workspace_stats']['messages_exist']) == 7
    assert stats3['workspace_stats']['messages_exist'][6]['num_messages_exist'] == 0

    # Test banning ppl doesn't decrease message count

    requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member2['auth_user_id']]
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member2['token'],
        'dm_id': dm_info.json()['dm_id'],
        'message': "Hgeo"
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': member2['token'],
        'dm_id': dm_info.json()['dm_id'],
        'message': "geld"
    })

    requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })

    users_stats_response4 = requests.get(f'{config.url}/users/stats/v1', params={
        'token': owner['token']
    })

    assert users_stats_response4.status_code == 200
    stats4 = users_stats_response4.json()
    assert len(stats4['workspace_stats']['messages_exist']) == 9
    assert stats4['workspace_stats']['messages_exist'][7]['num_messages_exist'] == 1
    assert stats4['workspace_stats']['messages_exist'][8]['num_messages_exist'] == 2

    # Test


'''
def test_users_stats_standup(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]
    pass


def test_users_stats_sendlater(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]
    pass
'''
