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
    
def test_invalid_channel():
    '''
    Tests that input error is raise when:
    if channel doesn't exist (input is 5 with only 1 channel)
    or channel input isn't valid (channel_id < 0 or channel_id is not an int)
    '''
    channel_id = generate_channel()["channel_id"]
    with pytest.raises(InputError):
        assert message_send("token", 5, "Hello")
    with pytest.raises(InputError):
        assert message_send("token", -2, "Hi")
    with pytest.raises(InputError):
        assert message_send("token", "string", "Hi")
        
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

##length message < -1 or messages > 1000 --> input error
def test_invalid_length():
    '''
    Tests that input error is raise when:
    message is empty
    message_length > 1000
    message is not a string
    '''
    channel_id = generate_channel()["channel_id"]
    with pytest.raises(InputError):
        assert message_send("token", channel_id, "")
    with pytest.raises(InputError):
        assert message_send("token", channel_id, long_message())
    with pytest.raises(InputError):
        assert message_send("token", channel_id, 20)

##access error -> valid user but not in channel (i.e. not an owner or member)
def test_user_access_error():
    '''
    Tests that access error is raised when:
    user is valid but not in channel
    token is not valid (non string for now)
    '''
    channel_id = generate_channel()["channel_id"]   
    user_id = auth_register_v1("taylor@gmail.com":, "slater", "Taylor", "group") 
    ##this will need to be replaced with a token input later
    with pytest.raises(InputError):
        assert message_send(user_id, channel_id, "")
    with pytest.raises(InputError):
        assert message_send(100, channel_id, "")
        
        
def test_success():
    '''
    Test for success:
    - user_1 created, added to channel, test user_1
    - user_1 and user_2 created, user_2 invite to channel, test user_2
    - user_1, user_3 and user_3 added to channel, test user_3
    - Test correct message_id
    '''
    user_info = generate_channel()
    user_1 = user_info["user"]
    channel_id = user_info["channel_id"]
    assert message_send(user_1 , channel_id, "Hello World") == 1
    user_2 = auth_register_v1("taylor@gmail.com":, "slater", "Taylor", "group")
    channel_invite_v1(user_1["auth_user_id"], channel_id, user_2["auth_user_id"])
    assert message_send(user_2 , channel_id, "This is a public service announcement") == 2
    user_3 = auth_register_v1("xue@gmail.com":, "xue", "richard", "fsjfkl")
    channel_invite_v1(user_1["auth_user_id"], channel_id, user_3["auth_user_id"])      
    assert message_send(user_3 , channel_id, "This is a public service announcement") == 3        
    
