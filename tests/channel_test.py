from src import auth
from src.error import InputError, AccessError
from src import channel
from src import other
from src import message
import pytest



# Channel addowner tests

# Channel removeowner tests

# Channel leave tests
def channel_leave_v1_success_test():
    
    other.clear_v1() 
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    channel_one_info = channel.channel_create_v2(user_one_info['token'], 'general', True)
    channel.channel_leave_v1(user_one_info['token'], channel_one_info['channel_id'])
    

    
    channel_one_details = {
        'name'          :  'general',
        'is_public'     :   True,
        'owner_members' :   [],
        'all_members'   :   []
    }

    assert(channel.channel_details_v2(user_one_info['token'], channel_one_info['channel_id'])) == channel_one_details
    

# Assumes members joining thru channel_join_v2 are turned into normal members
def channel_leave_v1_success_multiple_test():
    other.clear_v1() 
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    user_two_info  = auth.auth_register_v2("second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2("third@gmail.com", "password", "first", "last")
    
    channel_one_info = channel.channel_create_v2(user_one_info['token'], 'general', True)
    channel.channel_join_v2(user_two_info['token'], channel_one_info['channel_id'])
    channel.channel_join_v2(user_three_info['token'], channel_one_info['channel_id'])
    
    
    channel.channel_leave_v1(user_three_info['token'], channel_one_info['channel_id'])
    
    
    channel_one_details = {
        'name'          :  'general',
        'is_public'     :   True,
        'owner_members' :   [user_one_info['auth_user_id']],
        'all_members'   :   [user_one_info['auth_user_id'], user_two_info['auth_user_id']]
    }
    
    assert(channel.channel_details_v2(user_one_info['token'], channel_one_info['channel_id'])) == channel_one_details
    
    
    channel.channel_leave_v1(user_two_info['token'], channel_one_info['channel_id'])
    
    
    new_channel_one_details = {
        'name'          :  'general',
        'is_public'     :   True,
        'owner_members' :   [user_one_info['auth_user_id']],
        'all_members'   :   [user_one_info['auth_user_id']]
    }
    
    assert(channel.channel_details_v2(user_one_info['token'], channel_one_info['channel_id'])) == new_channel_one_details
    
    
def channel_leave_v1_invalid_channel_test():
    
    other.clear_v1() 
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    with pytest.raises(InputError):
        channel.channel_leave_v1(user_one_info['token'], 999999999)
        

def channel_leave_v1_non_member_test():
    
    
    other.clear_v1() 
    user_one_info = auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    user_two_info  = auth.auth_register_v2("second@gmail.com", "password", "first", "last")

    channel_one_info = channel.channel_create_v2(user_one_info['token'], 'general', True)
    with pytest.raises(AccessError):
        channel.channel_leave_v1(user_two_info['token'], channel_one_info)
        
