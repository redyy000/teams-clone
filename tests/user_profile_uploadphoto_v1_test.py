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


def test_user_profile_uploadphoto_success(setup_users):

    # Currently implementation uses random strings for image names
    # Hence impossible to function test
    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 200
    assert photo_response.json() == {}
    '''
    response = requests.get(f"{config.url}/user/profile/v1", params={
        'token': owner['token'],
        'u_id': owner['auth_user_id'],
    })

    assert response.status_code == 200
    stats = response.json()['user']
    assert stats['profile_img_url'] == f'{config.url}static/'
    '''


def test_user_profile_uploadphoto_invalid_token(setup_users):

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': 'woegoiwjegoiweoi',
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
        'x_start': 300,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 403


def test_user_profile_uploadphoto_non_jpg(setup_users):
    owner = setup_users[0]
    image_2 = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://i.imgur.com/CP6LCZT.png',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert image_2.status_code == 400


def test_user_profile_uploadphoto_fail_none(setup_users):
    owner = setup_users[0]
    image_2 = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': '',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert image_2.status_code == 400


def test_user_profile_uploadphoto_fail_false_url(setup_users):
    owner = setup_users[0]
    image_2 = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'gwoghoawhoi',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert image_2.status_code == 400


def test_user_profile_uploadphoto_fail_non_img_url(setup_users):
    owner = setup_users[0]
    image_2 = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://wikipedia.com',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100

    })

    assert image_2.status_code == 400


def test_user_profile_uploadphoto_x_small(setup_users):

    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
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
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
        'x_start': 0,
        'y_start': 300,
        'x_end': 100,
        'y_end': 100

    })

    assert photo_response.status_code == 400


def test_user_profile_uploadphoto_x_big(setup_users):

    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100000000,
        'y_end': 100

    })

    assert photo_response.status_code == 400


def test_user_profile_uploadphoto_y_big(setup_users):

    owner = setup_users[0]

    photo_response = requests.post(f'{config.url}/user/profile/uploadphoto/v1', json={
        'token': owner['token'],
        'img_url': 'https://i.imgur.com/bEwmq1s.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 10000000000

    })

    assert photo_response.status_code == 400
