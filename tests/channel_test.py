from src import auth
from src.error import InputError, AccessError
from src import channel
from src import other
from src import message
import pytest



# Channel addowner tests

def channel_addowner_success_test():
    other.clear_v1() 
    pass

# Channel removeowner tests
def channel_removeowner_success_test():
    other.clear_v1()
    pass

# Channel leave tests
def channel_leave_success_test():
    
    other.clear_v1() 
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    user_two_info  = auth.auth_register_v2("second@gmail.com", "password", "first", "last")
    channel_one_info = channel.channel_create_v2(user_one_info['token'], 'general', True)
    channel.channel_leave_v1(user_one_info['token'], channel_one_info['channel_id'])
    
    
    channel_one_details = {
        'name'          :  'general',
        'is_public'     :   True,
        'owner_members' :   [],
        'all_members'   :   []
    }

    assert(channel.channel_details_v2(user_one_info['token'], channel_one_info['channel_id'])) == channel_one_details
    
def channel
    
