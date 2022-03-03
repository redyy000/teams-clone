import pytest
from src.channels import channels_list_v1
from src.error import AccessError
from src.other import clear_v1

def test_invalid_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_list_v1(0)
        assert channels_list_v1("Invalid ID")
        assert channels_list_v1(1)

# If the user is part of 0 channels, there will be no return value (not an error)