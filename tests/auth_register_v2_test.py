from src import config
import pytest
import requests


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
# Returns a JSON file with status code and data
def initialise_test():
    '''
    Pytest fixture function to clear all records, and return a dummy user
    For testing purposes 
    '''
    # Calls clear on the saved data server-side
    requests.delete(f'{config.url}clear/v1')

    response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    return response


def register_user(email, password, name_first, name_last):
    '''
    Creates and sends a post request 

    Arguments:
        email (string)    - Email string that accepts regular expression
        password (string)    - Password for the email address, 6 or more characters long.
        name_first (string) - String containing first name, between 1-50 characters inclusive.
        name_last (string) - String containing last name, between 1-50 characters inclusive.

    Exceptions:
        None

    Return Value:
        {'username' : string } dictionary
    '''

    return requests.post(f'{config.url}auth/register/v2', json={'email': email,
                                                                'password': password,
                                                                'name_first': name_first,
                                                                'name_last': name_last})

    # Assert user is properly registered


def test_register_v2_success():

    requests.delete(f'{config.url}clear/v1')
    response = register_user('Elden@ring.com', 'password', 'John', 'Eldenring')
    # get user data
    assert response.status_code == 200

    '''
    data = response.json()
    # Check data is correct
    assert data[]
    '''


def test_register_v2_success_removed_user(setup_users):
    owner = setup_users[0]
    member1 = setup_users[1]
    # Remove george :(
    requests.delete(f"{config.url}/admin/user/remove/v1", json={
        'token': owner['token'],
        'u_id': member1['auth_user_id'],
    })

    response1 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': owner['token'],
        'u_id': member1['auth_user_id']
    })

    user_dict = response1.json()['user']
    assert response1.status_code == 200
    assert user_dict['email'] == ''
    assert user_dict['name_first'] == 'Removed'
    assert user_dict['name_last'] == 'user'
    assert user_dict['handle_str'] == ''

    # Asserting that removed handles and emails are reusable
    register_response = register_user(
        'rxue@gmail.com', 'password', 'richard', 'xue')
    assert register_response.status_code == 200

    response2 = requests.get(f"{config.url}/user/profile/v1", params={
        'token': owner['token'],
        'u_id': register_response.json()['auth_user_id']
    })

    user_dict = response2.json()['user']
    assert response2.status_code == 200
    assert user_dict['email'] == 'rxue@gmail.com'
    assert user_dict['name_first'] == 'richard'
    assert user_dict['name_last'] == 'xue'
    assert user_dict['handle_str'] == 'richardxue'


def test_register_v2_long_handle():

    requests.delete(f'{config.url}clear/v1')
    response = register_user('Elden@ring.com', 'password',
                             'John', 'SekiroDarkEldenBloodRingSoulsBorne')
    assert response.status_code == 200


def test_register_v2_duplicate_handle():
    requests.delete(f'{config.url}clear/v1')
    response1 = register_user('Elden@ring.com', 'password',
                              'John', 'John')
    response2 = register_user('Soul@dark.com', 'password',
                              'John', 'John')
    assert response1.status_code == 200
    assert response2.status_code == 200


def test_register_v2_invalid_email():
    requests.delete(f'{config.url}clear/v1')
    response = register_user('0010101010', 'password', 'John', 'Eldenring')
    assert response.status_code == 400


def test_register_v2_existing_email():
    requests.delete(f'{config.url}clear/v1')
    register_user('john@elden.com', 'password', 'John', 'Eldenring')
    register_user('james@elden.com', 'password', 'James', 'Eldenring')
    response = register_user(
        'james@elden.com', 'password', 'James', 'Darksoul')

    assert response.status_code == 400


def test_register_v2_password_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user('john@elden.com', '123', 'John', 'Eldenring')
    assert response.status_code == 400


def test_register_v2_name_first_long():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "password",
                             "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrf", "Smith")
    assert response.status_code == 400


def test_register_v2_name_first_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "password", "", "Smith")
    assert response.status_code == 400


def test_register_v2_name_last_long():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "abcohgeiou", "John",
                             "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrfhuhthatsweird")
    assert response.status_code == 400


def test_register_v2_name_last_short():
    requests.delete(f'{config.url}clear/v1')
    response = register_user("normal@gmail.com", "abc", "John", "")
    assert response.status_code == 400
