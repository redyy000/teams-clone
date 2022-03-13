import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_invite_v1, channel_messages_v1


def generate_channel():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    new_channel = channels_create_v1(user_id["auth_user_id"], "Discord", True)["channel_id"]
    return {"user": user_id, "channel_id": new_channel}

def generate_dm():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith")
    new_dm = dm_create_v1 = ("token", [user_id_2])
    message_id = message_senddm_v1("token", new_dm, "Hello World")
    return {"user": user_id, "dm_id": new_dm, "message_id": message_id}

def generate_owner_case_channel():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    new_channel = channels_create_v1(user_id["auth_user_id"], "Discord", True)["channel_id"]
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith") 
    message_id = message_send_v1("user2_token", new_channel, "Hello World")           
    message_remove_v1("valid_token", message_id)
    message_list = channel_messages_v1("valid_token", new_channel, 0) 
    return message_list
    
def generate_owner_case_dm():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith") 
    new_dm = dm_create_v1 = ("token", [user_id_2])    
    message_id = message_senddm_v1("user2_token", new_dm, "Hello World")           
    message_remove_v1("valid_token", message_id)
    message_list = dm_messages_v1("valid_token", new_dm, 0) 
    return message_list

def test_invalid_id():
    '''Tests that InputError Occurs if:
        - message_id does not exist
        - message_id is not an integer
    '''
    # Test case for channel
    test_info = generate_channel()
    with pytest.raises(InputError):
        assert message_remove_v1("token", 200)
    with pytest.raises(InputError):
        assert message_remove_v1("token", "string")
        
    # Test case for DMs
    test_info = generate_dm()
    with pytest.raises(InputError):
        assert message_remove_v1("token", 200)    
    with pytest.raises(InputError):
        assert message_remove_v1("token", "string")
        
def test_invalid_access():
    '''Tests AccessError if:
       - user token not a string
       - user not global owner and did not send message'''
       
    test_info = generate_channel()
    message_id = message_send_v1("user_token", test_info["new_channel"], "Hello World") 
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith") 
    with pytest.raises(AccessError):
        assert message_remove_test_v1("user_id_2_token",  message_id)
    with pytest.raises(AccessError):
        assert message_remove_test_v1("invalid_token",  message_id)
    with pytest.raises(AccessError):
        assert message_remove_test_v1(200,  message_id)
      
    test_info = generate_dm()
    message_id = message_send_v1("user_token", test_info["new_dm"], "Hello World") 
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith")     
    with pytest.raises(AccessError):
        assert message_remove_test_v1("user_id_2_token",  message_id)
    with pytest.raises(AccessError):
        assert message_remove_test_v1("invalid_token",  message_id)
    with pytest.raises(AccessError):
        assert message_remove_test_v1(200,  message_id) 

def test_success():
    '''Test success for
       - user sent message
       - user is an owner
    '''
    # Test case for channels
    test_info = generate_channel()
    message_list = test_info["message_list"]
    message_id = message_send_v1("user_token", test_info["new_channel"], "Hello World") 
    message_remove_v1("valid_token", message_id)
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) == {"name": "None"}
    
    test_info = generate_owner_case_channel()
    message_list = test_info["message_list"]
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) == {"name": "None"}
    
    # Test case for DMs
    test_info = generate_dm()
    message_list = test_info["message_list"]
    message_id = message_send_v1("user_token", test_info["new_dm"], "Hello World") 
    message_remove_v1("valid_token", message_id)
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) == {"name": "None"}    
  
    test_info = generate_owner_case_dm()
    message_list = test_info["message_list"]
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) == {"name": "None"}
'''
