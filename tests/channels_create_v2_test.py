import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src import config
import requests
import json


# Function to be used in tests
@pytest.fixture
def auth_user_id():
    requests.delete(f"{config.url}clear/v1")
    # creates a test user and returns auth_user_id
    data = requests.post(f"{config.url}auth/register/v2", json = {
        "email":"testemail@hotmail.com",
        "password": "testpassword123", 
        "name_first": "firstname", 
        "name_last": "lastname" 
    }).json()
    return data["token"]

# tests auth_user_id is valid
def test_channels_invalid_token(auth_user_id): 
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": "invalid token", 
        "name": "channel name",
         "is_public": True
        })    
    assert resp.status_code == 403
        
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": -1, 
        "name": "channel name 3",
         "is_public": True
        })
    assert resp.status_code == 403      
 

def test_channels_invalid_channel_name(auth_user_id):
    # tests invalid channel name if nothing entered or >20 characters --> "InputError"
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "",
         "is_public": True
        })
    assert resp.status_code == 400  
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "abcdefghijklmnopqrstuvwxyz",
         "is_public": True
        })
    assert resp.status_code == 400 
        
def test_channels_invalid_public_return(auth_user_id):
    # tests is_public return value is a boolean
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "channel name 4",
         "is_public": "No"
        })  
    assert resp.status_code == 400    
    resp = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "channel name 5",
         "is_public": 1
        })      
    assert resp.status_code == 400 

def test_channels_duplicate(auth_user_id):
    # tests for duplicate channel names
    requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "duplicate channel",
         "is_public": True
        })
    resp = requests.post(f"{config.url}channels/create/v2", json = 
            {
            "token": auth_user_id, 
            "name": "duplicate channel",
             "is_public": True
            }) 
    assert resp.status_code == 400 
        
def test_channels_success(auth_user_id):
    response = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "general",
         "is_public": True
        }) 
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'channel_id': 1}
    response = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "midnight-chats",
         "is_public": True
        })  
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["channel_id"] == 2   
    response = requests.post(f"{config.url}channels/create/v2", json = 
        {
        "token": auth_user_id, 
        "name": "questions",
         "is_public": True
        })        
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["channel_id"] == 3
    

