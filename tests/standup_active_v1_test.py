import pytest
import src.standup
import src.error
import threading
import json
import requests
import time
from src import config
from src import auth
from src import channels
from src import other
from src import standup
from datetime import timezone
import datetime



@pytest.fixture
def init():
    requests.delete(f'{config.url}clear/v1')    
    user1 = requests.post(f'{config.url}auth/register/v2', json={'email': "dlin@gmail.com",
                                                                     'password': "password",
                                                                     'name_first': "daniel",
                                                                     'name_last': "lin"}).json()
    channel1 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 1",
        'is_public': True
    }).json()   
    channel2 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 2",
        'is_public': True
    }).json()                   
    return {"user": user1['token'], "channel1": channel1["channel_id"], "channel2": channel2["channel_id"]}

def test_standup_active_channel_invalid(init):
    #channel id invalid --> input error
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })
    assert response.status_code == 200
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": 200,
    })
    assert response.status_code == 400
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": "invalid_name",
    })
    assert response.status_code == 400

def test_standup_active_invalid_token(init):
    #test token invalid --> access error
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })    
    assert response.status_code == 200
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": "invalid token",
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 403
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": 200,
        "channel_id": init["channel1"],
    })
    assert response.status_code == 403

def test_standup_active_user_invalid(init):
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movington@gmail.com",
                                                                     'password': "newpassword",
                                                                     'name_first': "max",
                                                                     'name_last': "ovington"}).json()
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })    
    assert response.status_code == 200
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": user2["token"],
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 403                                                                

def test_standup_active_success(init):
    ##coverage
    requests.post(f'{config.url}channels/create/v2', json={
        'token': init["user"],
        'name': "Channel 3",
        'is_public': True
    }) 
    #test nothing has been initialized
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
    #basic test --> should pass true for active
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })    
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    current_time = int(utc_time.timestamp() + 1.5)
    assert response.status_code == 200
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": True, "time_finish": current_time}
    #test status inactive
    time.sleep(1.5)
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}

    ##Test standup start does nothing when length is 0
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 0,   
    })
    assert response.status_code == 200
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": init["channel1"],  
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
    ##Coverage for testing
    response = requests.get(f'{config.url}standup/active/v1', params = {
        "token": init["user"],
        "channel_id": init["channel2"],  
    })
    assert response.status_code == 200
    assert response.json() == {"is_active": False, "time_finish": None}
