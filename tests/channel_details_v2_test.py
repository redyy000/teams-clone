import pytest
import requests
import json
from src import config
from src.user import user_profile_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src import channel_details_v2


# @pytest.fixture
# def clear_v1():
#     requests.delete(f'{config.url}clear/v1')


@pytest.fixture
def user1():
    '''
    Creates a test user and posts for use in testing.
    First user created, so global owner.
    Clears existing data
    '''
    requests.delete(f'{config.url}clear/v1')
    user_data1 = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'user1@gmail.com',
        'password': 'testpassword',
        'name_first': 'FirstName',
        'name_last': 'LastName',
    }).json()
    return user_data1['token']


@pytest.fixture
def user2():
    '''
    Creates a test user and posts for use in testing.
    '''
    user_data2 = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'user2@gmail.com',
        'password': 'testpassword2',
        'name_first': 'FirstName2',
        'name_last': 'LastName2',
    }).json()
    print(user_data2)
    return user_data2['token']


# @pytest.fixture
# def channel1(user1):
#     '''
#     Create a new channel for use in testing.
#     user1 is an owner.
#     Clears data.
#     '''
#     requests.delete(f'{config.url}clear/v1')
#     new_channel = requests.post(f"{config.url}channels/create/v2", json={
#         "token": user1,
#         "name": "New Channel",
#         "is_public": True
#     })
#     channel_data = new_channel.json()
#     return channel_data['channel_id']


def test_channel_details_v2_success(user1):
    '''
    Test to check correct response of a channel/details/v2 request
    '''
    new_channel1 = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1,
        "name": "New Channel",
        "is_public": True
    })

    response1 = requests.get(f'{config.url}channel/details/v2',
                             params={'token': user1, 'channel_id': new_channel1})
    response = response1.json()
    assert response == {
        'name': 'New Channel',
        'is_public': True,
        'owner_members': [{
            'u_id': user1['auth_user_id'],
            'email':user1['email'],
            'name_first':user1['name_first'],
            'name_last': user1['name_last'],
            'handle_str': user1['handle_str'],
        }],
        'all_members': [{
            'u_id': user1['auth_user_id'],
            'email':user1['email'],
            'name_first':user1['name_first'],
            'name_last': user1['name_last'],
            'handle_str': user1['handle_str'],
        }]
    }
    assert response.status_code == 200


def test_channel_details_v2_invalid_channel_id(user1):
    invalid_channel = requests.get(f'{config.url}channel/detailsv2', params={'token': user1,
                                                                             'channel_id': 7})
    assert invalid_channel.status_code == 400


def test_channel_details_v2_user_not_in_channel(user1, user2):
    new_channel2 = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1,
        "name": "New Channel",
        "is_public": True
    })
    print(f"new_channel2 has channel id: {new_channel2.json()}")
    channel_id2 = new_channel2.json()['channel_id']
    non_member = requests.get(f'{config.url}channel/details/v2', params={'token': user2,
                                                                         'channel_id': channel_id2})
    assert non_member.status_code == 403


def test_channel_details_v2_invalid_token(user1):
    new_channel3 = requests.post(f"{config.url}channels/create/v2", json={
        "token": user1,
        "name": "New Channel",
        "is_public": True
    })
    print(f"new_channel3 has channel id: {new_channel3.json()}")
    invalid_token = requests.get(f'{config.url}channel/details/v2', params={'token': 'invalid_token',
                                                                            'channel_id': new_channel3})
    assert invalid_token.status_code == 403
