
import re
from src.data_store import data_store
from src.error import InputError


'''

Given an email and a password, validate the given inputs and return the appropriate
auth_user_id, or throw an exception if the inputs are incorrect.

Arguments:
    email (string)    - Email string that accepts regular expression
    password (string)    - Password for the email address
    ...

Exceptions:
    InputError  - Occurs when password for a given email address is incorrect
    InputError  - Occurs when a given email does not exist

Return Value:
    Returns auth_user_id if email and email's password are both valid and correct
'''

def auth_login_v1(email, password):
    
    store = data_store.get()

    for user in store['users']:
        if user['email'] == email:
            if user['password'] == password:
                return {'auth_user_id': user['u_id']}
            else:
                raise InputError("Incorrect Password!")
    raise InputError("Email does not exist!")
        
        
    
'''

Given a name_first and name_last, create a new handle_str and return it
All handle_str made are unique to its user, and automatically changed
If a given handle_str already exists in the Datastore.

Arguments:
    store (Datastore)    - Data of all saved users
    name_first (string) - String containing first name, between 1-50 characters inclusive.
    name_last (string) - String containing last name, between 1-50 characters inclusive.


Exceptions:
   

Return Value:
    Returns newly created handle_str

'''

def create_handle_str(store, name_first, name_last):
    # Create handle_str
    concat_str = name_first.lower() + name_last.lower()
    handle_str = ''.join(char for char in concat_str if char.isalnum())
    if len(handle_str) > 20:
        handle_str = handle_str[0:20]
    
    # Check for duplicate handles...
    # Modify handle_str if duplicate exists.
    is_duplicate = True
    temp_handle_str = handle_str
    counter = 0
    while is_duplicate is True:
        for user in store['users']:
            if user['handle_str'] == temp_handle_str:
                temp_handle_str = handle_str + str(counter)
                counter += 1
                break
        else:
            is_duplicate = False
        
    if temp_handle_str != handle_str:
        handle_str = temp_handle_str
        
    return handle_str
    
    
'''


Given an email, password, name_first and name_last, create a new handle_str and auth_user_id
Proceed to save this new user as a dictionary containing the given inputs as well as handle_str and auth_user_id
Dictionary will enter the DataStore class as part of the dictionary key 'users' list. 

Arguments:
    email (string)    - Email string that accepts regular expression
    password (string)    - Password for the email address, 6 or more characters long.
    name_first (string) - String containing first name, between 1-50 characters inclusive.
    name_last (string) - String containing last name, between 1-50 characters inclusive.
    ...

Exceptions:
    InputError  - Occurs when name_first string is not between 1-50 characters inclusive.
    InputError  - Occurs when name_last string is not between 1-50 characters inclusive.
    InputError  - Occurs when email string is not a valid regular expression.
    InputError  - Occurs when email string matches an already existing entry. 
    InputError  - Occurs when password is not 6 or more characters long.
    

Return Value:
    Returns auth_user_id on successful creation of a new user entry.

'''

def auth_register_v1(email, password, name_first, name_last):
    
    store = data_store.get()
    
    # Determine if email matches regular expression.
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if (re.fullmatch(regex, email)) == None:
        raise InputError("Email does not match the regular expression!")
    
    # Determine if email already exists in users list.
    for user in store['users']:
        if user['email'] == email:
            raise InputError("Email already exists within system!")
        
    # Determine if password length is 6 or more letters long
    
    if len(password) < 6:
        raise InputError("Password is too short!")
        
    # Determine if name_first and name_last are appropriate lengths (1-50 char)
    # This will test name_first initially; if both first name and last name
    # Are incorrect, then only the first name error will be raised.
    if len(name_first) > 50 or len(name_first) <= 0:
        raise InputError("First name length is invalid!")
    elif len(name_last) > 50 or len(name_last) <= 0:
        raise InputError("Last name length is invalid!")
    
    
    # Create auth_user_id
    auth_user_id = len(store['users']) + 1
    
    # Create user dictionary
    user = {
        'u_id'  : auth_user_id,
        'email' : email,
        'password'   : password,
        'name_first' : name_first,
        'name_last'  : name_last,
        'handle_str' : create_handle_str(store, name_first, name_last)
    }
    
    store['users'].append(user)
    data_store.set(store)
    
    return {
        'auth_user_id': auth_user_id
    }
