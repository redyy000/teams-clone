import pytest
from src import auth
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store



# Test an error occurs with a non-regular expression email
def test_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        # Non-Regular Expression Email
        assert (auth.auth_register_v1("@@@@@", "Password", "First", "Last"))
        assert (auth.auth_register_v1("0000", "Password", "First", "Last"))
        
# Normal Tests to test valid inputs and output ids
# Output ids should be in ascending order from 1,2,3....
def test_valid():
    clear_v1()
    assert (auth.auth_register_v1("john@gmail.com", "johndarksoul", "John", "Darksoul")) == {'auth_user_id' : 1}
    assert (auth.auth_register_v1("54321abba12345@hotmail.com", "TakeaChance0nMe", "Abby", "Bartholomew")) == {'auth_user_id' : 2}
    assert (auth.auth_register_v1("z5555550@ad.unsw.edu.au", "Noma1dens?!#.(03e?&", "James", "Eldenring")) == {'auth_user_id' : 3}
    
# Test that the email already exists
def test_email_exists():
    clear_v1()
    assert (auth.auth_register_v1("George@gmail.com", "monkey", "George", "Monkey")) == {'auth_user_id' : 1}
    with pytest.raises(InputError):
        # Attempting to register with already used email.
        assert (auth.auth_register_v1("George@gmail.com", "banana", "George", "Banana"))

    
# Test password is 5 or less letters long
# Include password len == 0
def test_password_length_short():
    clear_v1()
    with pytest.raises(InputError):
        # 3 Letter long password
        assert(auth.auth_register_v1("normal@gmail.com", "abc", "John", "Smith"))
        # 5 Letter long password
        assert(auth.auth_register_v1("normal@gmail.com", "abcde", "John", "Smith"))
        # 0 Letter long password
        assert(auth.auth_register_v1("normal@gmail.com", "", "John", "Smith"))



# Test name_first is 51 characters long     
def test_name_first_length_long():
    clear_v1()
    with pytest.raises(InputError):
        assert(auth.auth_register_v1("normal@gmail.com", "abc", "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrf", "Smith"))
# Test name_first is 0 characters long

def test_name_first_length_short():
    clear_v1()
    with pytest.raises(InputError):
        assert(auth.auth_register_v1("normal@gmail.com", "abc", "", "Smith"))

# Test name_last is 51 characters long
def test_name_last_length_long():
    clear_v1()
    with pytest.raises(InputError):
        assert(auth.auth_register_v1("normal@gmail.com", "abc", "John", "mgubpezlxzrktxamqbrgizwdptqveadaykuffmplqnqiousnsrf"))
    
# Test name_last 0 characters long
def test_name_last_length_short():
    clear_v1()
    with pytest.raises(InputError):
        assert(auth.auth_register_v1("normal@gmail.com", "abc", "John", ""))

# Test for duplicate handles
# Not a blackbox test due to being forced to extract data from Datastore
# Each different group's implementation of Datastore would be impossible to account for.
def test_handle_duplicate():
    clear_v1()
    store = data_store.get()

    auth.auth_register_v1("one@gmail.com", "Password", "John", "Smith")
    auth.auth_register_v1("two@gmail.com", "Password", "John", "Smith")
    auth.auth_register_v1("three@gmail.com", "Password", "John", "Smith")
    auth.auth_register_v1("four@gmail.com", "Password", "John", "Smith")
    
    
    assert(store['users'][0]['handle_str']) == "johnsmith"
    assert(store['users'][1]['handle_str']) == "johnsmith0"
    assert(store['users'][2]['handle_str']) == "johnsmith1"
    assert(store['users'][3]['handle_str']) == "johnsmith2"
    
    

# Test a long (20+ chars) handle is shrunk to 20 characters 

def test_handle_long():
    clear_v1()
    store = data_store.get()
    auth.auth_register_v1("one@gmail.com", "Password", "LongLongLongLong", "MeebMaabMuub")
    auth.auth_register_v1("two@gmail.com", "Password", "LongLongLongLong", "MeebMaabMuub")
    assert(store['users'][0]['handle_str']) == "longlonglonglongmeeb"
    assert(len(store['users'][0]['handle_str'])) == 20
    
# Test that a duplicate handle is allowed to exceed 20 characters after shrinkage.
def test_handle_duplicate_length():
    clear_v1()
    store = data_store.get()
    auth.auth_register_v1("one@gmail.com", "Password", "LongLongLongLong", "MeebMaabMuub")
    auth.auth_register_v1("two@gmail.com", "Password", "LongLongLongLong", "MeebMaabMuub")
    assert(len(store['users'][0]['handle_str'])) == 20
    assert(len(store['users'][1]['handle_str'])) == 21