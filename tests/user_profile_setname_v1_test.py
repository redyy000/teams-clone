from platformdirs import user_cache_dir
import pytest
from src.error import InputError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.server import user_profile_setname_v1

'''
Test functions for user_profile_setname_v1. Tests for:
    - Invalid user (token invalid)
    - Setting empty name
    - Setting a name that is too long
    - Setting a name that is not a string
    - user_profile_setname_v1 is successful at changing a user's name
'''


def test_invalid_user():
    '''
    Tests if user token is valid i.e. if user exists
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # token invalid/doesn't exist
        assert user_profile_setname_v1(
            "invalid_token", "FirstName", "LastName")
    with pytest.raises(InputError):
        # token not a string
        assert user_profile_setname_v1(3, "FirstName", "LastName")


def test_blank_setname():
    '''
    Tests if the first name and/or last name is not empty
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # invalid/blank first name
        assert user_profile_setname_v1(user["token"], "", "LastName")
    with pytest.raises(InputError):
        # invalid/blank last name
        assert user_profile_setname_v1(user["token"], "FirstName", "")


def test_long_setname():
    '''
    Tests if the first and/or last name is more than 50 characters
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # long first name > 50
        assert user_profile_setname_v1(
            user["token"], "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "LastName")
    with pytest.raises(InputError):
        # long last name > 50
        assert user_profile_setname_v1(
            user["token"], "FirstName", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    with pytest.raises(InputError):
        #both > 50
        assert user_profile_setname_v1(user["token"], "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                                       "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


def test_setname_not_string():
    '''
    Tests if the name entered is a string
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # first name not a string
        assert user_profile_setname_v1(user["token"], 1, "LastName")
    with pytest.raises(InputError):
        # last name not a string
        assert user_profile_setname_v1(user["token"], "FirstName", 1)
    with pytest.raises(InputError):
        # both names not a string
        assert user_profile_setname_v1(user["token"], 1, 2)


def test_setname_successful():
    '''
    Tests if user_profile_setname_v1
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    user_profile_setname_v1(user["token"], "NewFirst", "NewLast")
    assert user_profile_v1(user["name_first"]) == "NewFirst"
    assert user_profile_v1(user["name_last"]) == "NewLast"
