import pytest
import requests
from src import config


OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2
INVALID_PERMISSION = 3


def test_admin_userpermissions_change__v1_success():

    requests.delete(f"{config.url}/clear/v1")

    # First user created, therefore owner and permission ID = 1
    owner_user = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'owner1gmail.com',
        'password': 'ownerpassword',
        'name_first': 'OwnerFirst',
        'name_last': 'OwnerLast',
    })
    assert owner_user.status_code == 200

    member_user = requests.post(f"{config.url}/auth/register/v2", json={
        'email': 'member1@gmail.com',
        'password': 'memberpassword',
        'name_first': 'MemberFirst',
        'name_last': 'MemberLast',
    })
    assert member_user.status_code == 200

    member_data = member_user.json()

    change_permission_id = requests.post(f"{config.url}/admin/userpermission/change/v1", json={
        'token': member_data['token'],
        'u_id': member_data['auth_user_id'],
        'permission_id': 1})

    assert change_permission_id.status_code == 200
    assert change_permission_id.json() == {}


def test_admin_userpermission_change_v1_invalid_user():
    # InputError 400
    pass


def test_admin_userpermission_change_v1_only_global_owner_demotion():
    # InputError 400
    pass


def test_admin_userpermission_change_v1_invalid_permission_id():
    # InputError 400
    pass


def test_admin_userpermission_change_v1_already_has_permission():
    # InputError 400
    pass


def test_admin_userpermission_change_v1_not_global_owner():
    # AccessError 403
    pass
