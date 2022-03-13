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
    message_id = message_send_v1("token", new_channel, "Hello World")
    return {"user": user_id, "channel_id": new_channel, "message_id": message_id}
    
def generate_owner_case_channel():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    new_channel = channels_create_v1(user_id["auth_user_id"], "Discord", True)["channel_id"]
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith") 
    message_id = message_send_v1("user2_token", new_channel, "Hello World")           
    message_edit_v1("valid_token", new_channel, "Changed Message")
    message_list = channel_messages_v1("valid_token", new_channel, 0) 
    return message_list
    
def generate_owner_case_dm():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith") 
    new_dm = dm_create_v1 = ("token", [user_id_2])    
    message_id = message_senddm_v1("user2_token", new_dm, "Hello World")           
    message_edit_v1("valid_token", new_dm, "Changed Message")
    message_list = dm_messages_v1("valid_token", new_channel, 0) 
    return message_list
    
def long_message():
    return """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA                                
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA                                
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
                   
def generate_dm():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith")
    new_dm = dm_create_v1 = ("token", [user_id_2])
    message_id = message_senddm_v1("token", new_dm, "Hello World")
    return {"user": user_id, "dm_id": new_dm, "message_id": message_id}
    
def test_invalid_message():
    '''
    Tests that InputError occurs if:
    - length of message over 1000 characters
    - message is not a string
    '''
    test_info = generate_channel()
    message_id = message_send_v1("user2_token", test_info["new_channel"], "Hello World")    
    with pytest.raises(InputError)
        assert message_edit_v1("token", test_info["message_id"], long_message())
    with pytest.raises(InputError)
        assert message_edit_v1("token", test_info["message_id"], 200)
    test_info = generate_dm()
    message_id = message_senddm_v1("user2_token", test_info["new_dm"], "Hello World")    
    with pytest.raises(InputError)
        assert message_edit_v1("token", test_info["dm_id"], long_message())
    with pytest.raises(InputError)
        assert message_edit_v1("token", test_info["dm_id"], 200)        
    
    
def test_invalid_id():
    '''tests that AccessError occurs if:
    - message was not sent by user and user does not have owner permissions"
    - user input i.e. token is invalid
    '''
    # Testng for Message Channels
    test_info = generate_channel()
    with pytest.raises(AccessError)
        assert message_edit_v1("invalid_token", test_info["message_id"], "Test Message")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith")
    with pytest.raises(AccessError)  
         assert message_edit_v1("user_2_token", test_info["message_id"], "Test Message")       
    with pytest.raises(AccessError)  
         assert message_edit_v1(200, test_info["message_id"], "Test Message")  
         
    # Testing for DMs             
    test_info = generate_dm()   
    with pytest.raises(AccessError)
        assert message_edit_v1("invalid_token", test_info["dm_id"], "Test Message")
    user_id_2 = auth_register_v1("Hsmith@gmail.com", "numpyyyy", "Hadyen", "Smith")
    with pytest.raises(AccessError)  
         assert message_edit_v1("user_2_token", test_info["dm_id"], "Test Message")       
    with pytest.raises(AccessError)  
         assert message_edit_v1(200, test_info["dm_id"], "Test Message")     
    
def test_success():
    '''Things to be tested here:
        works for user who sent message
        works for user who is a global owner to send message
    
        DMs - works for user who sent message
        DMs - works for owner
    '''
    # Testing for messages in Channels
    test_info = generate_channel()
    message_list = test_info["message_list"]
    message_edit_v1("valid_token", test_info["channel_id"], "Changed Message")
    message_list = channel_messages_v1("valid_toke", test_info["message_id"], 0)
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) != {"name": "None"}
    
    test_info = generate_owner_case_channel()
    message_list = test_info["message_list"]
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) != {"name": "None"}
    
    
    # Testing for messages in DMs
    test_info = generate_dm()
    message_list = test_info["message_list"]
    message_edit_v1("valid_token", test_info["dm_id"], "Changed Message")
    message_list = dm_messages_v1("valid_toke", test_info["dm_id"], 0)   
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) != {"name": "None"}    
    
    test_info = generate_owner_case_dm()
    message_list = test_info["message_list"]
    assert if next((x for x in message_list if x["message"] == "Changed Message"), {"name": "None"}) != {"name": "None"}    


