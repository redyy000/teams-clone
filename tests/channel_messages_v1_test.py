import pytest
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_invite_v1, channel_messages_v1

# Test the channel id is invalid
def test_channel_id_invalid():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")
    user_id_2 = auth_register_v1("Xue@gmail.com", "password", "Richard", "Nixon")
    user_id_3 = auth_register_v1("chicken@gmail.com", "AIENSW", "Marc", "Chee")
    new_channel = channels_create_v1(user_id["auth_user_id"], "Discord", True)
    assert user_id_2["auth_user_id"] == 2
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_2["auth_user_id"])
    with pytest.raises(InputError):
        assert channel_messages_v1(user_id["auth_user_id"], 500, 0)
        assert channel_messages_v1(user_id_2["auth_user_id"], "invalid", 0) 
    

# Test the channel index is greater than the message list or invalid
def test_channel_index_invalid():
    clear_v1()
    user_id = auth_register_v1("max@gmail.com", "ovington", "Ox", "Movington")    
    new_channel = channels_create_v1(user_id["auth_user_id"], "Reddit", True)
    with pytest.raises(InputError):
        assert channel_messages_v1(user_id["auth_user_id"], new_channel["channel_id"], 20)
        assert channel_messages_v1(user_id["auth_user_id"], new_channel["channel_id"], -200) 
        assert channel_messages_v1(user_id["auth_user_id"], new_channel["channel_id"], "notanint")     
    
# Test the user is valid but not in channel or is an invalid input
def test_channel_member_invalid():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "12345678", "Hayden", "Smith")
    user_id_2 = auth_register_v1("hello@gmail.com", "password", "Jake", "Renzella")
    user_id_3 = auth_register_v1("chicken@gmail.com", "AIENSW", "Marc", "Chee")
    new_channel = channels_create_v1(user_id["auth_user_id"], "Netflix", True)
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_2["auth_user_id"])
    with pytest.raises(AccessError):
        assert channel_messages_v1(200, new_channel["channel_id"], 0)
        assert channel_messages_v1(200, new_channel["channel_id"], 0)
        assert channel_messages_v1("invalid", new_channel["channel_id"], 0)        
    
    
# Test successful message 
def test_channel_message_success():
    clear_v1()
    user_id = auth_register_v1("123@gmail.com", "12345678", "Number", "Man")
    user_id_2 = auth_register_v1("567@gmail.com", "342984", "Count", "Dracula")
    user_id_3 = auth_register_v1("8994@gmail.com", "AIENSW", "Kanye", "West")
    new_channel = channels_create_v1(user_id["auth_user_id"], "7Prime", True)
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_2["auth_user_id"])
    assert channel_messages_v1(user_id["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}
    assert channel_messages_v1(user_id_2["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}  
    clear_v1()
    user_id = auth_register_v1("123@gmail.com", "12345678", "Number", "Man")
    user_id_2 = auth_register_v1("567@gmail.com", "342984", "Count", "Dracula")
    user_id_3 = auth_register_v1("8994@gmail.com", "AIENSW", "Kanye", "West")
    new_channel = channels_create_v1(user_id["auth_user_id"], "7Prime", True)
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_2["auth_user_id"])
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_3["auth_user_id"])
    assert channel_messages_v1(user_id["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}
    assert channel_messages_v1(user_id_2["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}
    assert channel_messages_v1(user_id_3["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}
    clear_v1()
    user_id = auth_register_v1("123@gmail.com", "12345678", "Number", "Man")
    user_id_2 = auth_register_v1("567@gmail.com", "342984", "Count", "Dracula")
    new_channel = channels_create_v1(user_id["auth_user_id"], "7Prime", True)
    new_channel_2 = channels_create_v1(user_id["auth_user_id"], "Foxtel", True)
    channel_invite_v1(user_id["auth_user_id"], new_channel["channel_id"], user_id_2["auth_user_id"])
    channel_invite_v1(user_id["auth_user_id"], new_channel_2["channel_id"], user_id_2["auth_user_id"])
    assert channel_messages_v1(user_id_2["auth_user_id"], new_channel["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}
    assert channel_messages_v1(user_id_2["auth_user_id"], new_channel_2["channel_id"], 0) == {"messages": [[]], "start": 0, "end": -1}  
    
 

