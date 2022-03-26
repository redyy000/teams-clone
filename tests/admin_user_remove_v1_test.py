from math import remainder
import pytest
import requests
from src import config


OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2
INVALID_PERMISSION = 3


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


def test_admin_user_remove_success(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    assert response.status_code == 200
    assert response.json() == {}

# NEEDS FUNCTIONALITY TESTS
# def test_admin_user_remove_func(setup_users):


def test_admin_user_remove_invalid_token(setup_users):

    member1 = setup_users[1]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': 'ahwgiohwoghowi',
        'u_id': member1['auth_user_id'],
    })

    assert response.status_code == 403


def test_admin_user_remove_invalid_u_id(setup_users):

    owner = setup_users[0]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': 99999999
    })

    assert response.status_code == 400


def test_admin_user_remove_only_global_owner(setup_users):

    owner = setup_users[0]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': owner['auth_user_id'],
    })

    assert response.status_code == 400


def test_admin_user_remove_token_non_authorised(setup_users):

    member1 = setup_users[1]
    member2 = setup_users[2]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': member1['token'],
        'u_id': member2['auth_user_id'],
    })

    assert response.status_code == 403


def test_admin_user_remove_from_channel(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # Create a channel for owner
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })
    # Member 1 Joins
    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id': channel_response.json()['channel_id']
    })

    assert join_response.status_code == 200

    # Member 2 Joins
    join2_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member2['token'],
        'channel_id': channel_response.json()['channel_id']
    })

    assert join2_response.status_code == 200

    # Member 2 posts messages
    requests.post(f"{config.url}message/send/v1", json={
        "token": member2['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Sekiro is better than elden ring'
    })

    # Member 1 posts messages
    requests.post(f"{config.url}message/send/v1", json={
        "token": member1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": member1['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'PUT YOUR AMBITIONS TO REST'
    })
    # Ban member 1
    remove_response1 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    # Ban member 2
    remove_response2 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })

    assert remove_response1.status_code == 200
    assert remove_response1.json() == {}

    assert remove_response2.status_code == 200
    assert remove_response2.json() == {}

    # Assert messages are all turned into 'Removed user'

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    message_list = messages_response.json()['messages']
    for message_dict in message_list:
        assert message_dict['message'] == 'Removed user'


def test_admin_user_remove_token(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    remove_response1 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    assert remove_response1.status_code == 200

    # Check the removed user cannot use their token anymore

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "general",
        "is_public": True
    })

    assert channel_response.status_code == 403


def test_admin_user_remove_from_channel_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # Create a channel for owner
    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    # Member 1 Joins
    join1_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id': channel_response.json()['channel_id']
    })

    assert join1_response.status_code == 200

    # Member 2 Joins
    join2_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member2['token'],
        'channel_id': channel_response.json()['channel_id']
    })

    assert join2_response.status_code == 200

    # Add member 1 and 2 as owners
    add_owner_response1 = requests.post(f"{config.url}channel/addowner/v1", json={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'user_id': member1['auth_user_id']})
    assert add_owner_response1.status_code == 200

    add_owner_response2 = requests.post(f"{config.url}channel/addowner/v1", json={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'user_id': member2['auth_user_id']})
    assert add_owner_response2.status_code == 200

    # Ban member 2 :(

    remove_response2 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })
    # Ban member 1 :(
    remove_response1 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })

    assert remove_response1.status_code == 200
    assert remove_response2.status_code == 200


def test_admin_user_remove_from_dm(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # Create DM
    dm_response = requests.post(f"{config.url}dm/create/v1", json={
        "token": owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })
    # Member 1 posts messages
    requests.post(f"{config.url}message/senddm/v1", json={
        "token": member1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'Every soul has its dark'
    })

    requests.post(f"{config.url}message/senddm/v1", json={
        "token": member1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'PUT YOUR AMBITIONS TO REST'
    })

    # Remove member1
    remove_response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    assert remove_response.status_code == 200
    assert remove_response.json() == {}

    # Assert messages are all turned into 'Removed user'

    messages_response = requests.get(f'{config.url}/dm/messages/v1', params={
        'token': owner['token'],
        'dm_id': dm_response.json()['dm_id'],
        'start': 0
    })

    message_list = messages_response.json()['messages']
    for message_dict in message_list:
        assert message_dict['message'] == 'Removed user'


def test_admin_user_remove_from_dm_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    # Create DM, where member2 is the dm owner
    dm_response = requests.post(f"{config.url}dm/create/v1", json={
        "token": member2['token'],
        'u_ids': [owner['auth_user_id'], member1['auth_user_id']]
    })

    assert dm_response.status_code == 200
    # Member 1 posts messages
    requests.post(f"{config.url}message/senddm/v1", json={
        "token": member1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'Every soul has its dark'
    })

    requests.post(f"{config.url}message/senddm/v1", json={
        "token": member1['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'PUT YOUR AMBITIONS TO REST'
    })
    # Member 2 sends messages
    requests.post(f"{config.url}message/senddm/v1", json={
        "token": member2['token'],
        "dm_id": dm_response.json()['dm_id'],
        "message": 'gjeohgeoijhgoiehoihgoihoiehg wow'
    })
    # Ban member 2 :(
    remove_response2 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })
    # Ban member 1 :(
    remove_response1 = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
    })

    assert remove_response1.status_code == 200
    assert remove_response2.status_code == 200
