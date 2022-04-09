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


'''
def test_user_profile_uploadphoto_success(setup_users):
    pass
    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': '',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 200
    assert photo_response.json() == {}

'''


def test_user_profile_uploadphoto_x_small(setup_users):

    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': '',
        'x_start': 300,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 400


def test_user_profile_uploadphoto_y_small(setup_users):

    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': '',
        'x_start': 0,
        'y_start': 300,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 400
