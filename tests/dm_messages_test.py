import pytest
import requests
from src import config


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
