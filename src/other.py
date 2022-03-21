import pickle
import src.server
import requests
from flask import Flask, request
from pathlib import Path
from src.data_store import data_store
from json import dumps

def store_data(data):
    '''
    Input Types:
    data --> dicionary (may be empty)
    
    Given a set of data, overwrite data.p with new data
    '''
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(data))

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
