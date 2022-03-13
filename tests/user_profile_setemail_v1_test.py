from platformdirs import user_cache_dir
import pytest
from src.error import InputError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.server import user_profile_setemail_v1
'''
Test functions for user_profile_setemail_v1. Tests for:
    - Invalid user (token invalid)
    - Set current email to blank/empty email
    - Set current to invalid email
    - Email already being used by another user
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
        assert user_profile_setemail_v1(
            "invalid_token", "user@gmail.com")
    with pytest.raises(InputError):
        # token not a string
        assert user_profile_setemail_v1(3, "user@gmail.com")


def test_blank_email():
    '''
    Tests whether the proposed email is a valid email.
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # Attempting to change a valid email to one that is invalid
        assert user_profile_setemail_v1(
            user["token"], "")


def test_invalid_email():
    '''
    Tests whether the email is in the correct email format, i.e. is a valid email
    '''
    clear_v1()
    user = auth_register_v1(
        "user@gmail.com", "password", "FirstName", "LastName")
    with pytest.raises(InputError):
        # Missing the @
        assert user_profile_setemail_v1(user["token"], "invalid.com")
    with pytest.raises(InputError):
        # Missing .com
        assert user_profile_setemail_v1(user["token"], "invalid@gmail")


def test_email_already_exists():
    '''
    Tests for changing an email to one that is already used by another user
    '''
    clear_v1()
    user_george = auth_register_v1("George@gmail.com", "monkey",
                                   "George", "Monkey")
    user_bob = auth_register_v1("canwefixit@gmail.com", "yeswecan",
                                "Bob", "Builder")
    with pytest.raises(InputError):
        # Attempting to change an email with an already used email
        # i.e. change George's email to one used by Bob
        assert user_profile_setemail_v1(
            user_george["token"], "canwefixit@gmail.com")


def test_user_profile_setemail_successful():
    '''
    Asserts a successful change of email
    '''
    clear_v1()
    user = auth_register_v1("user@gmail.com", "password",
                            "FirstName", "LastName")
    user_edited = auth_register_v1(
        "edited_user_email@gmail.com", "password", "FirstName", "LastName")

    assert user_profile_v1(user["email"]) == "edited_user_email@gmail.com"
