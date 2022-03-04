import pytest
from src import auth
from src.error import InputError
from src.other import clear_v1

# Test successful login
# Ensure given id is accurate
def test_success():
    clear_v1()
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    auth.auth_register_v1("two@email.com", "Wordpass", "Max", "Ovington")
    auth.auth_register_v1("three@email.com", "Secret", "Daniel", "Lin")
    assert(auth.auth_login_v1("one@email.com", "Password")) == {'auth_user_id' : 1}
    assert(auth.auth_login_v1("three@email.com", "Secret")) == {'auth_user_id' : 3}
    assert(auth.auth_login_v1("two@email.com", "Wordpass")) == {'auth_user_id' : 2}

# Test email does not exist
def test_email_false():
    clear_v1()
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    with pytest.raises(InputError):
        # Non-existant email with existing password
        assert(auth.auth_login_v1("false@email.com", "Password"))
        # Non-existant email with non-existing password
        assert(auth.auth_login_v1("fake@email.com", "Wordpass"))
        

# Test password is false
def test_password_false():
    clear_v1()
    auth.auth_register_v1("one@email.com", "Password", "Richard", "Xue")
    auth.auth_register_v1("two@email.com", "Wordpass", "Max", "Ovington")
    with pytest.raises(InputError):
        # Existing email with non-existant password
        assert(auth.auth_login_v1("one@email.com", "WrongPassword"))
        # Existing email with another email's password
        assert(auth.auth_login_v1("two@email.com", "Password"))