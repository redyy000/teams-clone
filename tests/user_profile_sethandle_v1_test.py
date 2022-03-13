from platformdirs import user_cache_dir
import pytest
from src.error import InputError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.server import user_profile_sethandle_v1

'''
Test functions for user_profile_sethandle_v1. Tests for:
    - Invalid user (token invalid)
    - Setting handle less than 3 characters
    - Setting handle more than 20 characters
    - Handle containing non-alphanumeric characters
    - Handle already used
    - user_profile_sethandle_v1 is successful at changing a user's handle
'''


def test_invalid_user():
    '''
    Tests if user token is valid i.e. if user exists
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        # token invalid/doesn't exist
        assert user_profile_sethandle_v1(
            "invalid_token", "FirstLast")
    with pytest.raises(InputError):
        # token not a string
        assert user_profile_sethandle_v1(3, "FirstLast")


def test_short_handle():
    '''
    Test if handle is less than 3 characters
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        # Setting a short handle, < 3 characters
        assert user_profile_sethandle_v1(
            user["token"], "ew")


def test_long_handle():
    '''
    Test if handle is more than 20 characters
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        # Setting a short handle, < 3 characters
        assert user_profile_sethandle_v1(
            user["token"], "onetwothreefourfivesix")


def test_handle_non_alphanumeric():
    '''
    Test if handle is more than 20 characters
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "First", "Last")
    with pytest.raises(InputError):
        # Setting a non-alphanumerical handle
        assert user_profile_sethandle_v1(user["token"], "one&two")


def test_handle_already_exists():
    clear_v1()
    user_george = auth_register_v1("George@gmail.com", "monkey",
                                   "George", "Monkey")
    user_bob = auth_register_v1("canwefixit@gmail.com", "yeswecan",
                                "Bob", "Builder")
    with pytest.raises(InputError):
        # Try setting George's handle to Bob's handle
        assert user_profile_sethandle_v1(
            user_george["token"], user_bob["handle_str"])


def test_user_profile_sethandle_successful():
    '''
    Asserts a successful change of handle
    '''
    clear_v1()
    user = auth_register_v1("user@gmail.com", "password",
                            "FirstName", "LastName")
    user_profile_sethandle_v1(user, "newhandle")
    assert user_profile_v1(user["handle_str"]) == "newhandle"
