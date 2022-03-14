from src import auth
from src.error import InputError, AccessError
from src import user
from src import other
import pytest


# User All Tests
# USER PROFILE DATA STRUCTURE
'''
user = {
        'u_id'  : auth_user_id,
        'email' : email,
        'name_first' : name_first,
        'name_last'  : name_last,
        'handle_str' : create_handle_str(store, name_first, name_last)
    }
'''
    
    
def user_profile_success_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    
    user_one_profile = {
        'user' :  {
            'u_id'  : 1,
            'email' : 'first@gmail.com',
            'name_first' : "first",
            'name_last'  : "last",
            'handle_str' : 'firstlast'
        }
    }


    assert(user.user_profile_v1(user_one_info['token'], user_one_info['auth_user_id'])) == user_one_profile
    
    
def user_profile_invalid_user():
    
    other.clear_v1()
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    
    with pytest.raises(InputError):
        assert(user.user_profile_v1(user_one_info['token'], 999999))