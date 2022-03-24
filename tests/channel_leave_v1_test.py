import pytest
import requests
from src import config

@pytest.fixture
def initialise_member():
    '''
    A short pytest fixture.
    Clears data store and registers a user.
    '''
    requests.delete(f'{config.url}clear/v1')
    register = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@email.com',
                                                                    'password': 'password',
                                                                    'name_first': 'first_name',
                                                                    'name_last': 'last_name'})
    return register

def initialise_channel(token):
    '''
    A short pytest fixture.
    Initialises a channel.
    '''
    channel = requests.post(f"{config.url}channels/create/v2", json= {'token': token,
                                                                      'name': 'General',
                                                                      'is_public': True})
    return channel

def test_channel_leave_v1_simple_success(initialise_member):
    register = initialise_member.json()
    token = register['token']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                    'password': 'justjack001',
                                                                    'name_first': 'bing',
                                                                    'name_last': 'rong'})
    user2 = register.json()
    u_id2 = user2['auth_user_id']
    token2 = user2['token']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                                   'channel_id': channel_id,
                                                                   'u_id': u_id2})

    leave = requests.post(f"{config.url}channel/leave/v1", json= {'token': token,
                                                                  'channel_id': channel_id})
    assert leave.status_code == 200
    details = requests.get(f'{config.url}channel/details/v2', params= {'token': token2,
                                                                       'channel_id': channel_id})
    details_data = details.json()
    assert details_data == {'name': 'General',
                            'is_public': True,
                            'owner_members': [],
                            'all_members': [{'email': 'test@bing.com',
                            'handle_str': 'bingrong',
                            'name_first': 'bing',
                            'name_last': 'rong',
                            'u_id': 2}]}
