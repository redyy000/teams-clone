import pytest
from src.auth import auth
from src.error import InputError
from data_store import clear_v1

# Test successful login
# Ensure given id is accurate
def test_success():
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    auth.auth_register_v1("two@email.com", "Wordpass", "Max", "Ovington")
    auth.auth_register_v1("three@email.com", "Secret", "Daniel", "Lin")
    assert(auth.auth_login_v1("one@email.com", "Password")) == 1
    assert(auth.auth_login_v1("three@email.com", "Secret")) == 3
    assert(auth.auth_login_v1("two@email.com", "Wordpass")) == 2

# Test email does not exist
def test_email_false():
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    with pytest.raises(InputError):
        # Non-existant email with existing password
        assert(auth.auth_login_v1("false@email.com", "Password"))
        

# Test password is false
def test_password_false():
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    auth.auth_register_v1("two@email.com", "Wordpass", "Max", "Ovington")
    with pytest.raises(InputError):
        # Existing email with non-existant password
        assert(auth.auth_login_v1("one@email.com", "WrongPassword"))
        
        
    with pytest.raises(InputError):
        # Existing email with another email's password
        assert(auth.auth_login_v1("two@email.com", "Password"))