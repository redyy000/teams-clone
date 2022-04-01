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


def test_user_stats_success(setup_users):
    owner = setup_users[0]
    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response.status_code == 200


def test_user_stats_invalid_token(setup_users):
    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': 'wehjgowheoighjwioeghoiwhegio'
    })

    assert user_stat_response.status_code == 403


def test_user_stats_functionality(setup_users):
    pass
    owner = setup_users[0]
    user_stat_response = requests.get(f'{config.url}/user/stats/v1', params={
        'token': owner['token'],
    })

    assert user_stat_response.status_code == 200
    assert user_stat_response.json()['user_stats'] == 2


# More user stats tests with extra options.......
