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


@pytest.fixture
def post_test_user():
    return test_user()


def test_user():
    requests.delete(f"{config.url}/clear/v1")
    '''
    Creates a test user and posts for use in http testing.
    '''
    post_test_user = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'user@gmail.com',
        'password': 'password',
        'name_first': 'FirstName',
        'name_last': 'LastName',
    })
    user_data = post_test_user.json()
    return user_data


@pytest.fixture
def fixture_george():
    return post_george()


@pytest.fixture
def fixture_bob():
    return post_bob()


@pytest.fixture
def post_dm_create():
    post_info = test_user()
    george_info = post_george()
    bob_info = post_bob()
    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_info['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    return post_info


def post_george():
    '''
    Creates test user named George Monkey, email george@gmail.com.
    '''
    post_george = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'george@gmail.com',
        'password': 'monkey',
        'name_first': 'George',
        'name_last': 'Monkey',
    })
    george_data = post_george.json()
    return george_data


def post_bob():
    '''
    Creates test user named Bob Builder, email canwefixit@gmail.com .
    '''
    post_bob = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'canwefixit@gmail.com',
        'password': 'yeswecan',
        'name_first': 'Bob',
        'name_last': 'Builder',
    })
    bob_data = post_bob.json()
    return bob_data


def test_dm_messages_success(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'message': "Hello World"})

    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 0
    })

    assert dm_messages.status_code == 200


def test_dm_messages_invalid_token(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })
    # Needs send messages.....
    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': 'clearly false token',
        'dm_id': dm_id.json()['dm_id'],
        'start': 0

    })

    assert dm_messages.status_code == 403


def test_dm_messages_invalid_dm_id(post_test_user, fixture_bob, fixture_george):

    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': 999999999,
        'start': 0

    })

    assert dm_messages.status_code == 400


def test_dm_messages_invalid_start(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 10000

    })

    assert dm_messages.status_code == 400


def test_dm_messages_start_one_one_message(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'message': 'bruh '})

    # Since there is 1 message and start is 1, result should be empty list
    messages_response = requests.get(f'{config.url}/dm/messages/v1', params={
        'token': owner['token'],
        'dm_id': dm.json()['dm_id'],
        'start': 1
    })

    message_list = messages_response.json()
    assert message_list['start'] == 1
    assert message_list['end'] == -1
    assert len(message_list['messages']) == 0
    assert messages_response.status_code == 200


def test_dm_messages_unauthorised_user(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'message': "Hello World"})

    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': fixture_george['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 0
    })

    assert dm_messages.status_code == 403


def test_dm_messages_functionality(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    requests.post(f'{config.url}message/senddm/v1', json={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'message': "Hello World"})

    dm_messages = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 0
    })
    assert dm_messages.status_code == 200
    ######


def test_dm_messages_functionality_multiple(post_test_user, fixture_bob, fixture_george):
    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    dm_id2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    # Put 50 msgs in dm1
    for idx in range(0, 50):
        requests.post(f'{config.url}message/senddm/v1', json={
            'token': post_test_user['token'],
            'dm_id': dm_id1.json()['dm_id'],
            'message': "Hello World"})

    # Put 50 msgs in dm2
    for idx in range(0, 50):
        requests.post(f'{config.url}message/senddm/v1', json={
            'token': post_test_user['token'],
            'dm_id': dm_id2.json()['dm_id'],
            'message': "Hello World"})

    dm_messages1 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id1.json()['dm_id'],
        'start': 0
    })

    # Checks that msg ids are based on all total msgs in all dms/channels
    # Similar to a global msg id var

    assert dm_messages1.status_code == 200
    dm_messages1_info = dm_messages1.json()['messages']
    for idx in range(0, 50):
        assert dm_messages1_info[idx]['message_id'] == 50 - idx
        assert dm_messages1_info[idx]['u_id'] == post_test_user['auth_user_id']
        assert dm_messages1_info[idx]['message'] == "Hello World"

    dm_messages2 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id2.json()['dm_id'],
        'start': 0
    })

    assert dm_messages2.status_code == 200
    dm_messages2_info = dm_messages2.json()['messages']
    for idx in range(0, 50):
        assert dm_messages2_info[idx]['message_id'] == 100 - idx
        assert dm_messages2_info[idx]['u_id'] == post_test_user['auth_user_id']
        assert dm_messages2_info[idx]['message'] == "Hello World"


def test_dm_messages_functionality_120(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })
    # First 25 Messages
    for idx in range(0, 25):
        requests.post(f'{config.url}message/senddm/v1', json={
            'token': fixture_bob['token'],
            'dm_id': dm_id.json()['dm_id'],
            'message': "Goodbye World"})
    # Next 50 Messages
    for idx in range(0, 50):
        requests.post(f'{config.url}message/senddm/v1', json={
            'token': post_test_user['token'],
            'dm_id': dm_id.json()['dm_id'],
            'message': "Hello World"})
    # Next 50 Messages
    for idx in range(0, 50):
        requests.post(f'{config.url}message/senddm/v1', json={
            'token': fixture_bob['token'],
            'dm_id': dm_id.json()['dm_id'],
            'message': "Evening World"})

    dm_messages1 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 0
    })

    dm_messages2 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 50
    })

    dm_messages3 = requests.get(f'{config.url}dm/messages/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id'],
        'start': 100
    })

    assert dm_messages1.status_code == 200
    dm_messages1_info = dm_messages1.json()['messages']
    assert len(dm_messages1_info) == 50

    for idx in range(0, 50):
        assert dm_messages1_info[idx]['message_id'] == 125 - idx
        assert dm_messages1_info[idx]['u_id'] == fixture_bob['auth_user_id']
        assert dm_messages1_info[idx]['message'] == "Evening World"

    assert dm_messages1.json()['end'] == 50
    assert dm_messages1.json()['start'] == 0

    assert dm_messages2.status_code == 200
    dm_messages2_info = dm_messages2.json()['messages']
    assert len(dm_messages2_info) == 50

    for idx in range(0, 50):
        assert dm_messages2_info[idx]['message_id'] == 75 - idx
        assert dm_messages2_info[idx]['u_id'] == post_test_user['auth_user_id']
        assert dm_messages2_info[idx]['message'] == "Hello World"

    assert dm_messages2.json()['end'] == 100
    assert dm_messages2.json()['start'] == 50

    assert dm_messages3.status_code == 200
    dm_messages3_info = dm_messages3.json()['messages']
    assert len(dm_messages3_info) == 25
    for idx in range(0, 25):
        assert dm_messages3_info[idx]['message_id'] == 25 - idx
        assert dm_messages3_info[idx]['u_id'] == fixture_bob['auth_user_id']
        assert dm_messages3_info[idx]['message'] == "Goodbye World"

    assert dm_messages3.json()['end'] == -1
    assert dm_messages3.json()['start'] == 100
