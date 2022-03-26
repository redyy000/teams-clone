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


def test_admin_userpermissions_change__v1_success(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    assert change_permission_id.status_code == 200
    assert change_permission_id.json() == {}

    change_permission_id2 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': member1['token'],
        'u_id': member2['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    assert change_permission_id2.status_code == 200
    assert change_permission_id2.json() == {}


def test_admin_userpermissions_change__v1_multiple_owners(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    change_permission_id1 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    change_permission_id2 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': member1['token'],
        'u_id': member2['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    # Tests func works
    assert change_permission_id1.status_code == 200
    assert change_permission_id2.status_code == 200
    assert change_permission_id1.json() == {}
    assert change_permission_id2.json() == {}


def test_admin_userpermissions_change__v1_change_owner_to_member(setup_users):

    owner = setup_users[0]
    member1 = setup_users[1]
    member2 = setup_users[2]

    change_permission_id1 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    change_permission_id2 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': member1['token'],
        'u_id': owner['auth_user_id'],
        'permission_id': MEMBER_PERMISSION})

    change_permission_id3 = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member2['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    assert change_permission_id1.status_code == 200
    assert change_permission_id2.status_code == 200
    assert change_permission_id3.status_code == 403


def test_admin_userpermissions_change__v1_invalid_token(setup_users):

    member1 = setup_users[1]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': 'woeifhwofhwoiehjfiow',
        'u_id': member1['auth_user_id'],
        'permission_id': OWNER_PERMISSION})

    assert change_permission_id.status_code == 403


def test_admin_userpermission_change_v1_invalid_user(setup_users):
    # InputError 400
    owner = setup_users[0]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': 9999999,
        'permission_id': OWNER_PERMISSION})

    assert change_permission_id.status_code == 400


def test_admin_userpermission_change_v1_only_global_owner_demotion(setup_users):
    # InputError 400

    owner = setup_users[0]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': owner['auth_user_id'],
        'permission_id': MEMBER_PERMISSION})

    assert change_permission_id.status_code == 400


def test_admin_userpermission_change_v1_invalid_permission_id(setup_users):
    # InputError 400

    owner = setup_users[0]
    member1 = setup_users[1]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
        'permission_id': 999})

    assert change_permission_id.status_code == 400


def test_admin_userpermission_change_v1_already_has_permission(setup_users):
    # InputError 400
    owner = setup_users[0]
    member1 = setup_users[1]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
        'permission_id': MEMBER_PERMISSION})

    assert change_permission_id.status_code == 400


def test_admin_userpermission_change_v1_not_global_owner(setup_users):
    # AccessError 403

    owner = setup_users[0]
    member1 = setup_users[1]

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': member1['token'],
        'u_id': owner['auth_user_id'],
        'permission_id': MEMBER_PERMISSION})

    assert change_permission_id.status_code == 403
