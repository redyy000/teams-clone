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
def post_dm_create():
    post_info = test_user()
    george_info = post_george()
    bob_info = post_bob()
    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_info['token'],
        'u_ids': [bob_info['auth_user_id'], george_info['auth_user_id']]
    })

    return post_info


@pytest.fixture
def fixture_george():
    return post_george()


@pytest.fixture
def fixture_bob():
    return post_bob()


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


def test_dm_details_success(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id'], fixture_george['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}/dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id.json()['dm_id']
    })
    assert dm_details.status_code == 200

    assert dm_details.json()[
        'name'] == 'bobbuilder, firstnamelastname, georgemonkey'


def test_dm_details_multiple(post_test_user, fixture_bob, fixture_george):

    dm_id1 = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id'], fixture_george['auth_user_id']]
    })

    dm_id2 = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    dm_details1 = requests.get(f'{config.url}/dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id1.json()['dm_id']
    })

    assert dm_details1.status_code == 200
    assert dm_details1.json()[
        'name'] == 'bobbuilder, firstnamelastname, georgemonkey'

    assert len(dm_details1.json()['members']) == 3

    for member_dict in dm_details1.json()['members']:
        if member_dict['u_id'] == post_test_user['auth_user_id']:
            assert member_dict['email'] == "user@gmail.com"
            assert member_dict['name_first'] == "FirstName"
            assert member_dict['name_last'] == "LastName"
            assert member_dict['handle_str'] == "firstnamelastname"
        if member_dict['u_id'] == fixture_bob['auth_user_id']:
            assert member_dict['email'] == "canwefixit@gmail.com"
            assert member_dict['name_first'] == "Bob"
            assert member_dict['name_last'] == "Builder"
            assert member_dict['handle_str'] == "bobbuilder"
        if member_dict['u_id'] == fixture_george['auth_user_id']:
            assert member_dict['email'] == "george@gmail.com"
            assert member_dict['name_first'] == "George"
            assert member_dict['name_last'] == "Monkey"
            assert member_dict['handle_str'] == "georgemonkey"

    dm_details2 = requests.get(f'{config.url}/dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': dm_id2.json()['dm_id']
    })

    assert dm_details2.status_code == 200

    assert dm_details2.json()[
        'name'] == 'bobbuilder, firstnamelastname'

    assert len(dm_details2.json()['members']) == 2

    for member_dict in dm_details2.json()['members']:
        if member_dict['u_id'] == post_test_user['auth_user_id']:
            assert member_dict['email'] == "user@gmail.com"
            assert member_dict['name_first'] == "FirstName"
            assert member_dict['name_last'] == "LastName"
            assert member_dict['handle_str'] == "firstnamelastname"
        if member_dict['u_id'] == fixture_bob['auth_user_id']:
            assert member_dict['email'] == "canwefixit@gmail.com"
            assert member_dict['name_first'] == "Bob"
            assert member_dict['name_last'] == "Builder"
            assert member_dict['handle_str'] == "bobbuilder"


def test_dm_details_invalid_token(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id'], fixture_george['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': 'invalid token',
        'dm_id': dm_id.json()['dm_id']
    })

    assert dm_details.status_code == 403


def test_dm_details_invalid_dm_id(post_test_user, fixture_bob, fixture_george):

    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id'], fixture_george['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': 99999999
    })

    assert dm_details.status_code == 400


def test_dm_details_invalid_dm_id_string(post_test_user, fixture_bob, fixture_george):

    requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id'], fixture_george['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': post_test_user['token'],
        'dm_id': 'owiehgoweih'
    })

    assert dm_details.status_code == 400


def test_dm_details_non_dm_member(post_test_user, fixture_bob, fixture_george):

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': post_test_user['token'],
        'u_ids': [fixture_bob['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': fixture_george['token'],
        'dm_id': dm_id.json()['dm_id']
    })

    assert dm_details.status_code == 403


def test_dm_details_func(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    dm_id = requests.post(f'{config.url}dm/create/v1', json={
        'token': owner['token'],
        'u_ids': [member1['auth_user_id'], member2['auth_user_id']]
    })

    dm_details = requests.get(f'{config.url}dm/details/v1', params={
        'token': owner['token'],
        'dm_id': dm_id.json()['dm_id']
    })

    # Assert member info
    assert dm_details.json()['name'] == 'daniellin, richardxue, ryangodakanda'

    for member_dict in dm_details.json()['members']:
        if member_dict['u_id'] == owner['auth_user_id']:
            assert member_dict['email'] == "dlin@gmail.com"
            assert member_dict['name_first'] == "daniel"
            assert member_dict['name_last'] == "lin"
            assert member_dict['handle_str'] == "daniellin"
        if member_dict['u_id'] == member1['auth_user_id']:
            assert member_dict['email'] == "rxue@gmail.com"
            assert member_dict['name_first'] == "richard"
            assert member_dict['name_last'] == "xue"
            assert member_dict['handle_str'] == "richardxue"
        if member_dict['u_id'] == member2['auth_user_id']:
            assert member_dict['email'] == "ryan@gmail.com"
            assert member_dict['name_first'] == "ryan"
            assert member_dict['name_last'] == "godakanda"
            assert member_dict['handle_str'] == "ryangodakanda"
