import pytest

from src.auth import auth_register_v1
from src.channels import channels_list_v1
from src.error import InputError
from src.other import clear_v1

def auth_user_id():
    clear_v1()
    auth_user_id = auth_register_v1("Testemail@gmail.com", "testpassword22", "first", "last")['auth_user_id']
    return auth_user_id

def test_invalid_user_id():
    clear_v1()
    with pytest.raises(InputError):
        assert channels_list_v1(0)
        assert channels_list_v1("Invalid ID")
        assert channels_list_v1(1)

# If the user is part of 0 channels, there will be no return value (not an error)