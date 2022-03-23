import pytest
import requests
import json
from src import config
'''
    Takes in token, u_id, permission_id
'''

OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2
INVALID_PERMISSION = 3


@pytest.fixture
def clear_v1():
    requests.delete(f'{config.url}clear/v1')


@pytest.fixture
def user1():
    email = "user1@gmail.com"
    password = "testpassword1"
    firstname = "firstname"
    lastname = "lastname"
    user1 = requests.post(f'{config.url}/auth/register/v2',
                          json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return user1['token']


@pytest.fixture
def user2():
    email = "user2@gmail.com"
    password = "testpassword2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(f'{config.url}/auth/register/v2',
                         json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)


def test_admin_userpermission_change_success(clear_v1, user1):
    clear_v1()
    response1 = requests.post(f'{config.url}admin/userpermission/change/v1', json={
        'token': user1['token'], 'u_id': user1['auth_user_id'], 'permission_id': 1})
    response1 = requests.post(f'{config.url}admin/userpermission/change/v1', json={
        'token': user1['token'], 'u_id': user1['auth_user_id'], 'permission_id': 1})

    assert response1.json() == {}
    assert response1.status_code == 200


def test_admin_userpermission_change_not_global_owner(user2):
    '''
    Access error when authorised user is ot a global owner
    '''
    resp = requests.post(config.url + "admin/userpermission/change/v1", json={
                         'token': 'invalid.token.input', 'u_id': user2['auth_user_id'], 'permission_id': OWNER_PERMISSION})
    assert resp.status_code == 403


def test_admin_permissions_input_error(clear, user1):
    invalid_id = user1['auth_user_id'] + 1
    resp = requests.post(config.url + "admin/userpermission/change/v1", json={
                         'token': user1['token'], 'u_id': invalid_id, 'permission_id': OWNER_PERMISSION})
    assert resp.status_code == 400
