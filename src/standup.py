from src.data_store import data_store
from src.error import InputError, AccessError
from src.other import is_valid_token
from src.message import message_send_v1
from src.user import user_profile_v1
import time
import threading
from datetime import timezone
import datetime

'''
Proposed data structure for startups:

channel = : channel_id,
            'name': name,
            'owner_members': [auth_user_id],
            'all_members': [
             {'user_id': auth_user_id,  # add the owner to the members list
            'permission_id': 1}  # owner has permission_id = 1
             ],
            'is_public': is_public,
            'messages': []
            
            (+) 'standup': {
                            'is_active': bool,
                            'u_id': integer id,
                            'time_finish': unix timestamp,
                            'buffer': [{'u_id': integer id,'message': string]
                            }

'''

def reset_standup(channel_id):
    #load data
    store = data_store.get()
    
    #get channel and standup
    channel = next((c for c in store["channels"] if c["channel_id"] == channel_id), None)
    if channel == None:
        return 

    standup = channel["standup"]
    
    #clear standup data
    standup["is_active"] = False
    standup["u_id"] = 0
    standup["time_start"] = None
    standup["time_finish"] = None
    standup["buffer"] = []

    #store data
    data_store.set(store)

def standup_thread(token, channel_id, start):
    '''
    Operation for thread function
    '''
    #load data
    store = data_store.get()


    #get channel and standup
    channel = next((c for c in store["channels"] if c["channel_id"] == channel_id), None)
    if channel == None:
        return 

    standup = channel["standup"]

    if standup["time_start"] != start or standup["is_active"] == False:
        return

    #convert buffer to string
    message_str = ''
    for text in standup["buffer"]:
        user_exists = next((c for c in store["users"] if c["u_id"] == text["u_id"]), None)
        if user_exists != None:
            user = user_profile_v1(token, text["u_id"])["user"]
            handle = user['handle_str']
            message = text["message"]
            message_str += f"{handle}: {message}\n"

    #pass buffer as a paramter into message_send_v1()
    #if message_length == 0 do nothing
    if len(standup["buffer"]) > 0:
        message_send_v1(token, channel_id, message_str)

    #clear standup data
    standup["is_active"] = False
    standup["u_id"] = 0
    standup["time_finish"] = None
    standup["buffer"] = []

    #store data
    data_store.set(store)


def standup_start_v1(token, channel_id, length):
    '''
    Given a valid channel and valid token 
    Start a standup in the channel for X seconds
    determined by the 'length' parameter

    The standup buffers messages that are sent to the standup within the elasped
    time of the standup

    After the standup finishes the buffered messages are converted into one single message
    in the channel posted by the user who started the standup

    Returns the finished time as a unix timestamp (time_finish)

    Arguments:
        token --> auth_token of user
        channel_id --> channel id that the standup will start in
        length --> the length of the standup in seconds

    Exceptions:
        Input Error --> channel_id invalid
        Input Error --> length is negative
        Input Error --> a standup is already active
        Access Erorr --> User not in channel
        Access Error --> Invalid Token

    Return Value:
        time_finish
    '''
    #load data
    store = data_store.get()

    #check token
    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    user_id = payload['u_id']

    #check channel valid
    channels_list = store["channels"]

    if isinstance(channel_id, int) == False or channel_id > len(channels_list) \
            or channel_id <= 0:
        raise InputError(
            description=f"Channel_id {type(channel_id)} is not valid!")

    #check user not in channel
    user_found = False
    for channel in channels_list:
        if channel["channel_id"] == channel_id:
            curr_channel = channel
        for member in channel['all_members']:
            if member['user_id'] == user_id:
                user_found = True

    if user_found == False:
        raise AccessError(description = "f{user_id} not in channel!")

    #check standup not active
    standup = curr_channel["standup"]
    if standup["is_active"] == True:
        raise InputError(description = "A standup is already active!")

    #check length valid
    if isinstance(length, str) == True:
        raise InputError(description = "Standup length invalid")
    if length < 0:
        raise InputError(description = "Standup length invalid")

    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    start = utc_time.timestamp()

    #change startup status to active
    if length == 0:
        return {"time_finish": start}

    #set active status
    standup["is_active"] = True
    standup["u_id"] = user_id
    standup["time_finish"] = int(start + length)
    standup["time_start"] = start

    #create thread helper function passing seconds as time
    new_thread = threading.Timer(float(length), standup_thread, args=(token, channel_id, start))
    new_thread.start()

    #store data
    data_store.set(store)

    #return finishing time (now + length as unix)
    return {"time_finish": standup["time_finish"]}

def standup_active_v1(token, channel_id):
    '''
    Given a valid channel and valid token 
    check whether a return is active and return the status of the standup

    Arguments:
        token --> auth_token of user
        channel_id --> channel id that the standup will start in

    Exceptions:
        Input Error --> channel_id invalid
        Access Error --> Invalid Token
        Access Error --> User not in channel

    Return Value:
        is_active --> boolean value
        time_finish --> finishing time as a unix timestamp
    '''

    #load data
    store = data_store.get()

    #check token 
    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    user_id = payload['u_id']

    #check channel valid
    channels_list = store["channels"]

    if isinstance(channel_id, int) == False or channel_id > len(channels_list) \
            or channel_id <= 0:
        raise InputError(
            description=f"Channel_id {type(channel_id)} is not valid!")

    #check user not in channel
    user_found = False
    for channel in channels_list:
        if channel["channel_id"] == channel_id:
            curr_channel = channel
        for member in channel['all_members']:
            if member['user_id'] == user_id:
                user_found = True

    if user_found == False:
        raise AccessError(description = "f{user_id} not in channel!")

    #return status of standup
    standup = curr_channel["standup"]

    return {"is_active": standup["is_active"], "time_finish": standup["time_finish"]}

def standup_send_v1(token, channel_id, message):
    '''
    Given a valid channel and valid token and an active standup
    send a message to the standup buffer

    Arguments:
        token --> auth_token of user
        channel_id --> channel id that the standup will start in
        message --> string value of message

    Exceptions:
        Input Error --> channel_id invalid
        Input Error --> message length greater than 1000
        Input Error --> Standup is not currently active
        Access Error --> Invalid Token
        Access Error --> User not in channel

    Return Value:
        is_active --> boolean value
        time_finish --> finishing time as a unix timestamp
    '''

    #load data
    store = data_store.get()

    #check token
    payload = is_valid_token(token)
    if payload is False:
        raise AccessError(description="Invalid token")

    user_id = payload['u_id']

    #check channel valid
    channels_list = store["channels"]

    if isinstance(channel_id, int) == False or channel_id > len(channels_list) \
            or channel_id <= 0:
        raise InputError(
            description=f"Channel_id {type(channel_id)} is not valid!")

    #check user not in channel
    user_found = False
    for channel in channels_list:
        if channel["channel_id"] == channel_id:
            curr_channel = channel
        for member in channel['all_members']:
            if member['user_id'] == user_id:
                user_found = True
            
    if user_found == False:
        raise AccessError(description = "f{user_id} not in channel!")

    #check message length < 1000
    if isinstance(message, str) == False:
        raise InputError(description = f'Message type invalid!')
    if len(message) > 1000:
        raise InputError(description = f'Message: {message} length invalid!')    

    #check standup is active
    standup = curr_channel["standup"]
    if standup["is_active"] == False:
        raise InputError(description = "No standup is active in this channel!")

    #add dictionary to standup buffer
    message = {
        'u_id': user_id,
        'message': message
    }
    standup["buffer"].append(message)

    #store data
    data_store.set(store)

    return {}

