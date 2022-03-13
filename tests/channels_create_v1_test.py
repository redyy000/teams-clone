import pytest

from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

store = data_store.get


# Function to be used in tests
def auth_user_id():
    clear_v1()
    # creates a test user and returns auth_user_id
    auth_user_id = auth_register_v1('testemail@hotmail.com', 'testpassword123', 'firstname', 'lastname')['auth_user_id']
    return auth_user_id


def test_invalid_user_id(): 
    with pytest.raises(AccessError):
        clear_v1()
        auth_register_v1('user1@gmail.com', 'testuser1', 'user1first', 'user1last')
        auth_register_v1('user2@gmail.com', 'testuser2', 'user2first', 'user2last')
    # tests auth_user_id is valid
        assert channels_create_v1(3, 'channel name 1', True)
        assert channels_create_v1(0, 'channel name 2', True)
        assert channels_create_v1(-1, 'channel name 3', True)

def test_invalid_channel_name():
    clear_v1()
    # tests invalid channel name if nothing entered or >20 characters --> "InputError"
    auth_user_id()
    with pytest.raises(InputError):
        assert channels_create_v1(1, '', True)
        assert channels_create_v1(1, 'abcdefghijklmnopqrstuvwxyz', True)

def test_invalid_public_return():
    clear_v1()
    # tests is_public return value is a boolean
    auth_user_id()
    with pytest.raises(InputError):
        assert channels_create_v1(1, 'channel name 4', 'No')
        assert channels_create_v1(1, 'channel name 5', 1)


def test_channel_duplicate():
    clear_v1()
    # tests for duplicate channel names
    auth_user_id()
    channels_create_v1(1, 'duplicate channel', True)
    with pytest.raises(InputError):
        assert channels_create_v1(1, 'duplicate channel', True)
        
def test_channel_success():
    clear_v1()
    auth_user_id()
    assert(channels_create_v1(1, 'general', True)) == {'channel_id' : 1}
    assert(channels_create_v1(1, 'midnight-chats', True)) == {'channel_id' : 2}
    assert(channels_create_v1(1, 'questions', True)) == {'channel_id' : 3}