import pytest
from src import config
from src.auth import auth_register_v2
from src.channels import channels_list_v2, channels_listall_v2
from src.channels import channels_create_v2
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.channel import channel_invite_v2
import requests
import json

@pytest.fixture
def init_test():
    requests.delete(f"{config.url}clear/v1")
    data = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"test@gmail.com",
        "password": "123password", 
        "name_first": "John", 
        "name_last": "Doe" 
    }).json()["token"]    
    return data

# List Functions

def test_channels_list1(init_test):
    #short channels_list test
    user_id2 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json()    
    channel_id1 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "test_channel", 
        "is_public": True, 
    }).json()    
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":init_test,
        "channel_id": channel_id1['channel_id'], 
        "u_id": user_id2['auth_user_id'], 
    })
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id2['token']})
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 1, 'name': 'test_channel'}]
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id2['token']})    
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 1, 'name': 'test_channel'}]


def test_channels_list2(init_test):
    #long channels_list test
    user_id2 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json() 
    user_id3 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"realemail@gmail.com",
        "password": "safepassword", 
        "name_first": "Jeremy", 
        "name_last": "Doe" 
    }).json() 
    user_id4 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"real123@gmail.com",
        "password": "goodpassword", 
        "name_first": "John", 
        "name_last": "Smith" 
    }).json()  
    user_id5 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"throwaway@gmail.com",
        "password": "strongpassword", 
        "name_first": "Joanne", 
        "name_last": "Citizen" 
    }).json()    
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "General", 
        "is_public": True, 
    }).json() 
    channel_id2 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "Hidden", 
        "is_public": False, 
    }).json()     
    channel_id3 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":user_id4['token'],
        "name": "John and Joanne", 
        "is_public": True, 
    }).json()
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":user_id4['token'],
        "name": "John PRIVATE", 
        "is_public": False, 
    }).json()    
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":init_test,
        "channel_id": channel_id2['channel_id'], 
        "u_id": user_id2['auth_user_id'], 
    })    
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":user_id2['token'],
        "channel_id": channel_id2['channel_id'], 
        "u_id": user_id4['auth_user_id'], 
    })       
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":user_id4['token'],
        "channel_id": channel_id3['channel_id'], 
        "u_id": user_id5['auth_user_id'], 
    })     
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": init_test}) 
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 1, 'name': 'General'}, {'channel_id': 2, 'name': 'Hidden'}]
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id2['token']}) 
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 2, 'name': 'Hidden'}]
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id3['token']})      
    assert response.status_code == 200
    assert response.json()["channels"] == []
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id4['token']})
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 2, 'name': 'Hidden'}, {'channel_id': 3, 'name': 'John and Joanne'}, {'channel_id': 4, 'name': 'John PRIVATE'}]   
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": user_id5['token']})   
    assert response.status_code == 200 
    assert response.json()["channels"] == [{'channel_id': 3, 'name': 'John and Joanne'}]

def test_channels_list3(init_test):
    #tests invalid user ID
    requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json() 
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "General", 
        "is_public": True, 
    }).json() 
    response = requests.get(f"{config.url}channels/list/v2", params = {"token": 3})
    assert response.status_code == 403
        
# Listall Functions:        
        
def test_channels_listall1(init_test):
    #short channels_listall test
    user_id2 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json() 
    channel_id1 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "General", 
        "is_public": True, 
    }).json() 
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":init_test,
        "channel_id": channel_id1['channel_id'], 
        "u_id": user_id2['auth_user_id'], 
    })    
    response = requests.get(f"{config.url}channels/listall/v2", params = {"token": user_id2['token']})    
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 1, 'name': 'General'}]

def test_channels_listall2(init_test):
    #long channels_listall test
    user_id2 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json() 
    requests.post(f"{config.url}auth/register/v2", json = {
        "email":"realemail@gmail.com",
        "password": "safepassword", 
        "name_first": "Jeremy", 
        "name_last": "Doe" 
    }).json() 
    user_id4 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"real123@gmail.com",
        "password": "goodpassword", 
        "name_first": "John", 
        "name_last": "Smith" 
    }).json()  
    user_id5 = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"throwaway@gmail.com",
        "password": "strongpassword", 
        "name_first": "Joanne", 
        "name_last": "Citizen" 
    }).json()    
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "General", 
        "is_public": True, 
    }).json() 
    channel_id2 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "Hidden", 
        "is_public": False, 
    }).json()     
    channel_id3 = requests.post(f"{config.url}channels/create/v2", json = {
        "token":user_id4['token'],
        "name": "John and Joanne", 
        "is_public": True, 
    }).json()
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":user_id4['token'],
        "name": "John PRIVATE", 
        "is_public": False, 
    }).json()    
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":init_test,
        "channel_id": channel_id2['channel_id'], 
        "u_id": user_id2['auth_user_id'], 
    })    
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":user_id2['token'],
        "channel_id": channel_id2['channel_id'], 
        "u_id": user_id4['auth_user_id'], 
    })       
    requests.post(f"{config.url}channel/invite/v2", json = {
        "token":user_id4['token'],
        "channel_id": channel_id3['channel_id'], 
        "u_id": user_id5['auth_user_id'], 
    })     
    response = requests.get(f"{config.url}channels/listall/v2", params = {"token": init_test})   
    assert response.status_code == 200
    assert response.json()["channels"] == [{'channel_id': 1, 'name': 'General'}, {'channel_id': 2, 'name': 'Hidden'}, {'channel_id': 3, 'name': 'John and Joanne'}, {'channel_id': 4, 'name': 'John PRIVATE'}]

def test_channels_listall3(init_test):
    #tests invalid user ID
    requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json() 
    requests.post(f"{config.url}channels/create/v2", json = {
        "token":init_test,
        "name": "General", 
        "is_public": True, 
    }).json() 
    response = requests.get(f"{config.url}channels/listall/v2", params = {"token": 3})     
    assert response.status_code == 403

def test_channels_listall4(init_test):
    #tests for 0 channels
    requests.post(f"{config.url}auth/register/v2", json = {
        "email":"anothertest@gmail.com",
        "password": "securepassword", 
        "name_first": "Jane", 
        "name_last": "Doe" 
    }).json()
    response = requests.get(f"{config.url}channels/listall/v2", params = {"token": init_test})   
    assert response.status_code == 200
    assert response.json()["channels"] == []

