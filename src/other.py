import pickle
import src.server
import requests
from flask import Flask, request
from pathlib import Path
from src.data_store import data_store
from json import dumps
    
BASE_URL = "http://127.0.0.1:{config.port}"

def store_data(data):
    '''
    Input Types:
    data --> dicionary (may be empty)
    
    Given a set of data, overwrite data.p with new data
    '''
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(data))

@APP.route("/clear/v2", methods = ["DELETE"])
def clear_v1():
    '''
    Input Types:
    None
    
    Sets data in data.p to a default dictionary of empty lists
    '''
    DATA_STRUCTURE = {
        "users": [],
        "channels": [],
        "dms": [],
        "global_messages": [],
        "tokens": []
    }
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(DATA_STRUCTURE))  

def load_data():
    '''
    Input Types:
    None
    
    load_data from data.p as a readable data structure
    '''
    if Path("data.p").exists() == False:
        requests.delete(f"{BASE_URL}/clear/v2")
    with open("data.p", "rb") as FILE:
        return pickle.loads(FILE.read())
