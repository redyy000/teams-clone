import pytest
import requests
from src import config


# User All Tests
# USER PROFILE DATA STRUCTURE
'''
user = {
        'u_id'  : auth_user_id,
        'email' : email,
        'name_first' : name_first,
        'name_last'  : name_last,
        'handle_str' : create_handle_str(store, name_first, name_last),
        'session_id_list' : [1]
    }
'''


@pytest.fixture
def post_test_user():
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


def test_users_all_success_code(post_test_user):
    post_bob()
    post_george()

    list_response = requests.get(f"{config.url}/users/all/v1", json={
        'token': post_test_user['token']
    })

    assert list_response.status_code == 200


def test_users_all_success_functionality(post_test_user):

    bob_info = post_bob()
    george_info = post_george()

    list_response = requests.get(f"{config.url}/users/all/v1", json={
        'token': post_test_user['token']
    })

    user_list = list_response.json()['users']

    # How to check the list???

    for user_data in user_list:
        if user_data['user']['handle_str'] == 'bobbuilder':
            assert user_data['user']['email'] == 'canwefixit@gmail.com'
            assert user_data['user']['name_first'] == 'Bob'
            assert user_data['user']['name_last'] == 'Builder'
            assert user_data['user']['u_id'] == bob_info['auth_user_id']

        elif user_data['user']['handle_str'] == 'georgemonkey':
            assert user_data['user']['email'] == 'george@gmail.com'
            assert user_data['user']['name_first'] == 'George'
            assert user_data['user']['name_last'] == 'Monkey'
            assert user_data['user']['u_id'] == george_info['auth_user_id']

        elif user_data['user']['handle_str'] == 'firstnamelastname':
            assert user_data['user']['email'] == 'user@gmail.com'
            assert user_data['user']['name_first'] == 'FirstName'
            assert user_data['user']['name_last'] == 'LastName'
            assert user_data['user']['u_id'] == post_test_user['auth_user_id']


def test_users_all_invalid_token(post_test_user):

    list_response = requests.get(f"{config.url}/users/all/v1", json={
        'token': 'invalid token'
    })

    assert list_response.status_code == 400
