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

    user1_info = response1.json()
    user2_info = response2.json()
    user3_info = response3.json()
    userlist.append(user1_info)
    userlist.append(user2_info)
    userlist.append(user3_info)
    return userlist


def test_message_edit_success(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        "message": 'Ringo did nothing wrong'
    })

    assert edit_response.status_code == 200

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    assert messages_response.json(
    )['messages'][0]['message'] == 'Ringo did nothing wrong'


def test_message_edit_channel_notification(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        "message": '@daniellin bruh'
    })

    notification_member2 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member2.status_code == 200
    note2 = notification_member2.json()['notifications']

    assert len(note2) == 1
    assert note2[0]['notification_message'] == 'daniellin tagged you in general: @daniellin bruh'
    assert note2[0]['dm_id'] == -1
    assert note2[0]['channel_id'] == channel_response.json()['channel_id']
    assert edit_response.status_code == 200


def test_message_edit_dm_notification(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm1.json()['dm_id'],
        'message': "Hello World"})

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        "message": '@daniellin bruh'
    })

    assert dm1.status_code == 200

    notification_member2 = requests.get(f'{config.url}/notifications/get/v1', params={
        'token': owner['token']
    })

    assert notification_member2.status_code == 200
    note2 = notification_member2.json()['notifications']

    assert len(note2) == 1
    assert note2[0]['notification_message'] == 'daniellin tagged you in daniellin, richardxue, ryangodakanda: @daniellin bruh'
    assert note2[0]['dm_id'] == dm1.json()['dm_id']
    assert note2[0]['channel_id'] == -1
    assert edit_response.status_code == 200


def test_message_edit_invalid_token(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": 'woeighwoieghowheiogh',
        "message_id": message_response.json()['message_id'],
        "message": 'Ringo did nothing wrong'
    })

    assert edit_response.status_code == 403


def test_message_edit_non_existant_message_id(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response1 = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": 9999999,
        "message": 'Ringo did nothing wrong'
    })

    assert edit_response1.status_code == 400

    edit_response2 = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": 'eiogheiohgroie',
        "message": 'Ringo did nothing wrong'
    })

    assert edit_response2.status_code == 400


def test_message_edit_length_long(setup_users):
    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        "message": 'Ringo did nothing wrong' * 100
    })

    assert edit_response.status_code == 400

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    # Assert message has not changed
    assert messages_response.json(
    )['messages'][0]['message'] == 'Every soul has its dark'

# Tests for both non_sender and non_global owner/non_channel_owner


def test_message_edit_non_sender_non_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        "message": 'Ringo did nothing wrong'
    })

    assert edit_response.status_code == 403


def test_message_edit_channels_empty(setup_users):

    owner = setup_users[0]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f'{config.url}message/send/v1', json={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'message': 'bruh '})

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        'message': ''
    })

    assert edit_response.status_code == 200

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': setup_users[0]['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    assert len(messages_response.json()['messages']) == 0

    # Test message is gone....


def test_message_edit_dms_empty(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        'message': ''
    })

    assert edit_response.status_code == 200

    messages_response = requests.get(f'{config.url}/dm/messages/v1', params={
        'token': setup_users[0]['token'],
        'dm_id': dm.json()['dm_id'],
        'start': 0
    })

    message_list = messages_response.json()
    assert message_list['start'] == 0
    assert message_list['end'] == -1
    assert len(message_list['messages']) == 0
    assert messages_response.status_code == 200


def test_message_edit_dms_invalid_sender(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        'message': ''
    })

    assert edit_response.status_code == 403


def test_message_edit_dms_non_member(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': []
    })

    message_response = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        'message': ''
    })

    assert edit_response.status_code == 403


def test_message_edit_dms_success(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    message_response1 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': member1['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    message_response2 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'wogeihowighowehgoiwhoeighwoegowiheoig'})

    message_response3 = requests.post(f'{config.url}message/senddm/v1', json={
        'token': member2['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'wogeih'})

    edit_response1 = requests.put(f"{config.url}message/edit/v1", json={
        "token": member1['token'],
        "message_id": message_response1.json()['message_id'],
        'message': 'i could never be replaced'
    })

    edit_response2 = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response2.json()['message_id'],
        'message': 'ahahnooooooo'
    })

    edit_response3 = requests.put(f"{config.url}message/edit/v1", json={
        "token": member2['token'],
        "message_id": message_response3.json()['message_id'],
        'message': 'ahahaha u  are being replaced'
    })

    assert edit_response1.status_code == 200
    assert edit_response2.status_code == 200
    assert edit_response3.status_code == 200

    messages_response = requests.get(f'{config.url}/dm/messages/v1', params={
        'token': setup_users[0]['token'],
        'dm_id': dm.json()['dm_id'],
        'start': 0
    })

    # Assert the messages have been edited, with the identical ids
    message_list = messages_response.json()['messages']
    for message_dict in message_list:
        if message_dict['message'] == 'i could never be replaced':
            assert message_dict['message_id'] == message_response1.json()[
                'message_id']
        if message_dict['message'] == "ahahnooooooo":
            assert message_dict['message_id'] == message_response2.json()[
                'message_id']
        if message_dict['message'] == 'ahahaha u  are being replaced':
            assert message_dict['message_id'] == message_response3.json()[
                'message_id']


def test_message_edit_global_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": member1['token'],
        "name": "general",
        "is_public": True
    })

    message_response = requests.post(f'{config.url}message/send/v1', json={
        'token': member1['token'],
        'channel_id': channel_response.json()['channel_id'],
        'message': 'bruh '})
    assert message_response.status_code == 200

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': owner['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": owner['token'],
        "message_id": message_response.json()['message_id'],
        'message': 'every bruh has its dark'
    })

    assert edit_response.status_code == 200

    messages_response = requests.get(f'{config.url}/channel/messages/v2', params={
        'token': owner['token'],
        'channel_id': channel_response.json()['channel_id'],
        'start': 0
    })

    assert len(messages_response.json()['messages']) == 1
    assert messages_response.status_code == 200
    assert messages_response.json(
    )['messages'][0]['message'] == 'every bruh has its dark'


def test_message_remove_non_global_owner(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    channel_response = requests.post(f"{config.url}channels/create/v2", json={
        "token": owner['token'],
        "name": "general",
        "is_public": True
    })

    join_response = requests.post(f'{config.url}channel/join/v2', json={
        'token': member1['token'],
        'channel_id':  channel_response.json()['channel_id']
    })
    assert join_response.status_code == 200

    message_response = requests.post(f"{config.url}message/send/v1", json={
        "token": owner['token'],
        "channel_id": channel_response.json()['channel_id'],
        "message": 'Every soul has its dark'
    })

    edit_response = requests.put(f"{config.url}message/edit/v1", json={
        "token": member1['token'],
        "message_id": message_response.json()['message_id'],
        'message': 'every bruh has its dark'
    })

    assert edit_response.status_code == 403
