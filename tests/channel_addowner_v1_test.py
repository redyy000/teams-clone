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


def test_channel_addowner_v1_simple_success(initialise_member):
    register = initialise_member.json()
    token = register['token']
    u_id1 = register['auth_user_id']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'anothertest@gmail.com',
                                                                    'password': 'securepassword',
                                                                    'name_first': 'Jane',
                                                                    'name_last': 'Doe'})
    assert register2.status_code == 200
    u_id2 = register2.json()["auth_user_id"]
    test = requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                                   'channel_id': channel_id,
                                                                   'u_id': u_id2})
    assert test.status_code == 200
    
    addowner = requests.post(f"{config.url}channel/addowner/v1", json= {'token': token,
                                                                        'channel_id': channel_id,
                                                                        'u_id': u_id2})
    assert addowner.status_code == 200
    details = requests.get(f'{config.url}channel/details/v2', params= {'token': token,
                                                                       'channel_id': channel_id})
    details_data = details.json()
    assert details_data == {'name': 'General',
                            'is_public': True,
                            'owner_members': [{'u_id': u_id1,
                                             'email': 'test@email.com',
                                             'name_first': 'first_name',
                                             'name_last': 'last_name',
                                             'handle_str': 'firstnamelastname'},
                                             {'u_id': u_id2,
                                              'email': 'anothertest@gmail.com',
                                              'name_first': 'Jane',
                                              'name_last': 'Doe',
                                              'handle_str': 'janedoe'}
                                             ],
                            'all_members': [{'u_id': u_id1,
                                             'email': 'test@email.com',
                                             'name_first': 'first_name',
                                             'name_last': 'last_name',
                                             'handle_str': 'firstnamelastname'},
                                             {'u_id': u_id2,
                                              'email': 'anothertest@gmail.com',
                                              'name_first': 'Jane',
                                              'name_last': 'Doe',
                                              'handle_str': 'janedoe'}]}

