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
    channel3 = requests.post(f'{config.url}channels/create/v2', json={
        'token': user1['token'],
        'name': "Channel 3",
        'is_public': True
    }).json()                        
    return {"user": user1['token'], "channel1": channel1["channel_id"], "channel2": channel2["channel_id"], 'channel3': channel3["channel_id"]}

def test_standup_start_channel_invalid(init):
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": "Invalid Name",
        "length": 1.5,   
    })
    assert response.status_code == 400
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": 200,
        "length": 1.5,   
    })
    assert response.status_code == 400
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": -200,
        "length": 1.5,   
    })
    assert response.status_code == 400

def test_standup_start_invalid_length(init):
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": -200,   
    })
    assert response.status_code == 400
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": "invalid input",   
    })          
    assert response.status_code == 400

def test_standup_start_invalid_standup(init):
    requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })
    assert response.status_code == 400
    
def test_standup_start_invalid_user_access(init):
    #test user not in channel --> access error 
    user2 = requests.post(f'{config.url}auth/register/v2', json={'email': "movington@gmail.com",
                                                                     'password': "newpassword",
                                                                     'name_first': "Max",
                                                                     'name_last': "Ovington"}).json()
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": user2["token"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })  
    assert response.status_code == 403

def test_standup_start_invalid_token(init):
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": "token_invalid",
        "channel_id": init["channel1"],
        "length": 1.5,   
    })  
    assert response.status_code == 403
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": 2000,
        "channel_id": init["channel1"],
        "length": 1.5,   
    }) 
    assert response.status_code == 403

def test_standup_start_success_thread(init):
    #note set thread time < 3 seconds
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    current_time = utc_time.timestamp() + 1.5
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })
    #test successful endpoints
    assert response.status_code == 200
    #test by correct finish time
    assert response.json()["time_finish"] == int(current_time)
    #test another thread can be created after the standup has ended
    time.sleep(2)
    response = requests.post(f'{config.url}standup/start/v1', json = {
        "token": init["user"],
        "channel_id": init["channel1"],
        "length": 1.5,   
    })
    assert response.status_code == 200