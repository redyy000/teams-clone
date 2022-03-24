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


def test_admin_user_remove_success(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    assert response.status_code == 200


def test_admin_user_remove_invalid_token(setup_users):

    member1 = setup_users[1]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': 'ahwgiohwoghowi',
        'u_id': member1['auth_user_id'],
    })

    assert response.status_code == 403


def test_admin_user_remove_invalid_u_id(setup_users):

    owner = setup_users[0]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': 99999999
    })

    assert response.status_code == 400


def test_admin_user_remove_only_global_owner(setup_users):

    owner = setup_users[0]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': owner['auth_user_id'],
    })

    assert response.status_code == 400


def test_admin_user_remove_token_non_authorised(setup_users):

    member1 = setup_users[1]
    member2 = setup_users[2]

    response = requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': member1['token'],
        'u_id': member2['auth_user_id'],
    })

    assert response.status_code == 403
