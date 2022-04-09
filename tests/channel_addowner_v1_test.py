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
    channel = requests.post(f"{config.url}channels/create/v2", json={'token': token,
                                                                     'name': 'General',
                                                                     'is_public': True})
    return channel


def test_channel_addowner_v1_invalid_token(initialise_member):
    register = initialise_member.json()
    token = register['token']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                     'password': 'justjack001',
                                                                     'name_first': 'bing',
                                                                     'name_last': 'rong'})
    u_id2 = register2.json()['auth_user_id']
    addowner = requests.post(f"{config.url}channel/addowner/v1", json={'token': 3,
                                                                       'channel_id': channel_id,
                                                                       'u_id': u_id2})
    assert addowner.status_code == 403


def test_channel_addowner_v1_invalid_channel(initialise_member):
    register = initialise_member.json()
    token = register['token']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                     'password': 'justjack001',
                                                                     'name_first': 'bing',
                                                                     'name_last': 'rong'})
    u_id2 = register2.json()['auth_user_id']
    addowner = requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                                       'channel_id': 1,
                                                                       'u_id': u_id2})
    assert addowner.status_code == 400


def test_channel_addowner_v1_invalid_user(initialise_member):
    register = initialise_member.json()
    token = register['token']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    addowner = requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                                       'channel_id': channel_id,
                                                                       'u_id': 3})
    assert addowner.status_code == 400


def test_channel_addowner_v1_non_member(initialise_member):
    register = initialise_member.json()
    token = register['token']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                     'password': 'justjack001',
                                                                     'name_first': 'bing',
                                                                     'name_last': 'rong'})
    u_id2 = register2.json()['auth_user_id']
    addowner = requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                                       'channel_id': channel_id,
                                                                       'u_id': u_id2})
    assert addowner.status_code == 400


def test_channel_addowner_v1_owner(initialise_member):
    register = initialise_member.json()
    token = register['token']
    register['auth_user_id']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                     'password': 'justjack001',
                                                                     'name_first': 'bing',
                                                                     'name_last': 'rong'})
    u_id2 = register2.json()['auth_user_id']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                          'channel_id': channel_id,
                                                          'u_id': u_id2})
    requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                            'channel_id': channel_id,
                                                            'u_id': u_id2})
    addowner = requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                                       'channel_id': channel_id,
                                                                       'user_id': u_id2})
    assert addowner.status_code == 400


def test_channel_addowner_v1_no_owner_permissions(initialise_member):
    register = initialise_member.json()
    token = register['token']
    u_id1 = register['auth_user_id']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'anothertest@gmail.com',
                                                                     'password': 'securepassword',
                                                                     'name_first': 'Jane',
                                                                     'name_last': 'Doe'})
    u_id2 = register2.json()['auth_user_id']
    token2 = register2.json()['token']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                          'channel_id': channel_id,
                                                          'u_id': u_id2})
    register3 = requests.post(f"{config.url}auth/register/v2", json={'email': 'testagain@gmail.com',
                                                                     'password': 'newpassword',
                                                                     'name_first': 'John',
                                                                     'name_last': 'Win'})
    u_id3 = register3.json()['auth_user_id']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                          'channel_id': channel_id,
                                                          'u_id': u_id3})
    requests.post(f"{config.url}channel/addowner/v1", json={'token': token2,
                                                            'channel_id': channel_id,
                                                            'u_id': u_id3})
    details = requests.get(f'{config.url}channel/details/v2', params={'token': token,
                                                                      'channel_id': channel_id})
    details_data = details.json()
    assert details_data == {'name': 'General',
                            'is_public': True,
                            'owner_members': [{'u_id': u_id1,
                                               'email': 'test@email.com',
                                               'name_first': 'first_name',
                                               'name_last': 'last_name',
                                               'handle_str': 'firstnamelastname',
                                               'profile_img_url': ''}
                                              ],
                            'all_members': [{'u_id': u_id1,
                                             'email': 'test@email.com',
                                             'name_first': 'first_name',
                                             'name_last': 'last_name',
                                             'handle_str': 'firstnamelastname',
                                             'profile_img_url': ''},
                                            {'u_id': u_id2,
                                             'email': 'anothertest@gmail.com',
                                             'name_first': 'Jane',
                                             'name_last': 'Doe',
                                             'handle_str': 'janedoe',
                                             'profile_img_url': ''},
                                            {'u_id': u_id3,
                                             'email': 'testagain@gmail.com',
                                             'name_first': 'John',
                                             'name_last': 'Win',
                                             'handle_str': 'johnwin',
                                             'profile_img_url': ''}]}


def test_channel_addowner_v1_success(initialise_member):
    register = initialise_member.json()
    token = register['token']
    u_id1 = register['auth_user_id']
    variable = initialise_channel(token).json()
    channel_id = variable['channel_id']
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'anothertest@gmail.com',
                                                                     'password': 'securepassword',
                                                                     'name_first': 'Jane',
                                                                     'name_last': 'Doe'})
    u_id2 = register2.json()['auth_user_id']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                          'channel_id': channel_id,
                                                          'u_id': u_id2})
    requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                            'channel_id': channel_id,
                                                            'u_id': u_id2})
    details = requests.get(f'{config.url}channel/details/v2', params={'token': token,
                                                                      'channel_id': channel_id})
    details_data = details.json()
    assert details_data == {'name': 'General',
                            'is_public': True,
                            'owner_members': [{'u_id': u_id1,
                                               'email': 'test@email.com',
                                               'name_first': 'first_name',
                                               'name_last': 'last_name',
                                               'handle_str': 'firstnamelastname',
                                               'profile_img_url': ''},
                                              {'u_id': u_id2,
                                              'email': 'anothertest@gmail.com',
                                               'name_first': 'Jane',
                                               'name_last': 'Doe',
                                               'handle_str': 'janedoe',
                                               'profile_img_url': ''}
                                              ],
                            'all_members': [{'u_id': u_id1,
                                             'email': 'test@email.com',
                                             'name_first': 'first_name',
                                             'name_last': 'last_name',
                                             'handle_str': 'firstnamelastname',
                                            'profile_img_url': ''},
                                            {'u_id': u_id2,
                                             'email': 'anothertest@gmail.com',
                                             'name_first': 'Jane',
                                             'name_last': 'Doe',
                                             'handle_str': 'janedoe',
                                             'profile_img_url': ''}]}


def test_channel_addowner_v1_success2(initialise_member):
    register = initialise_member.json()
    token = register['token']
    u_id1 = register['auth_user_id']
    initialise_channel(token)
    register2 = requests.post(f"{config.url}auth/register/v2", json={'email': 'test@bing.com',
                                                                     'password': 'justjack001',
                                                                     'name_first': 'bing',
                                                                     'name_last': 'rong'})
    u_id2 = register2.json()['auth_user_id']
    channel2 = requests.post(f"{config.url}channels/create/v2", json={'token': token,
                                                                      'name': 'Channel 2',
                                                                      'is_public': True})
    channel_id2 = channel2.json()['channel_id']
    requests.post(f"{config.url}channel/invite/v2", json={'token': token,
                                                          'channel_id': channel_id2,
                                                          'u_id': u_id2})
    requests.post(f"{config.url}channel/addowner/v1", json={'token': token,
                                                            'channel_id': channel_id2,
                                                            'u_id': u_id2})

    details = requests.get(f'{config.url}channel/details/v2', params={'token': token,
                                                                      'channel_id': channel_id2})
    details_data = details.json()
    assert details_data == {'name': 'Channel 2',
                            'is_public': True,
                            'owner_members': [{'u_id': u_id1,
                                               'email': 'test@email.com',
                                               'name_first': 'first_name',
                                               'name_last': 'last_name',
                                               'handle_str': 'firstnamelastname',
                                               'profile_img_url': ''},
                                              {'u_id': u_id2,
                                              'email': 'test@bing.com',
                                               'name_first': 'bing',
                                               'name_last': 'rong',
                                               'handle_str': 'bingrong',
                                               'profile_img_url': ''}
                                              ],
                            'all_members': [{'u_id': u_id1,
                                             'email': 'test@email.com',
                                             'name_first': 'first_name',
                                             'name_last': 'last_name',
                                             'handle_str': 'firstnamelastname',
                                             'profile_img_url': ''},
                                            {'u_id': u_id2,
                                             'email': 'test@bing.com',
                                             'name_first': 'bing',
                                             'name_last': 'rong',
                                             'handle_str': 'bingrong',
                                             'profile_img_url': ''}]}


def test_channel_addowner_v1_non_global_nor_normal_owner(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]

    channel_id = requests.post(f'{config.url}channels/create/v2', json={
        'token': owner['token'],
        'name': 'general',
        'is_public': True
    })

    requests.post(f'{config.url}channel/invite/v2', json={
        'token': owner['token'],
        'channel_id': channel_id.json()['channel_id'],
        'u_id': member1['auth_user_id']
    })

    add_owner_response = requests.post(f"{config.url}channel/addowner/v1", json={
        'token': member1['token'],
        'channel_id': channel_id.json()['channel_id'],
        'u_id': member1['auth_user_id']})

    assert add_owner_response.status_code == 403
