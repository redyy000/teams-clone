from src import auth
from src.error import InputError
from src import dm
from src import other
import pytest


# Assumptions
# DMs have an unlimited amount of ppl in a group (u_id list)
# The creator is NOT in the u_id list
# The creator is the owner of the DM
# Name of the DM is generated based on the users of the DM
# Name should be alphabetically sorted, comma-and-space-separated list of 
# User handles

# dm_ids are increasing, from the number one onwards
# returned as a dictionary with key value 'dm_id'


# A = Owner
# B,C,D = Members

# Members: B,C,D
# Owner: A
# B,C,D, A = ALL MEMBERS

# Members = B,C,D 
# Dm_create returns B,C,D in the members key-value list
# Dm_create will 
# Dm_details returns A,B,C,D


# User A has token "AAAAAA"
# Given token "AAAAA", can the user A be identified?

# Function that given a token, returns u_id
# Put it in other_py

# 1. Function Tests
# 2. HTTP Tests

dm_data_structure = {
    # Name of dm automatically generated
    'name' : 'string',
    
    
    # List of normal member u_ids
    # Normal members == NOT owners
    'normal_members' : [],
    
    
    # List of owner u_ids
    # Original creator is first
    'owner' : [],
    
    # List of message dictionaries
    'messages' : [
        {
            
            # Messages_id is index of message list + 1
            # I.e. message_id of 1 is message_list[0]
            # message_id of 2 is message_list[1]
            'message_id' : int,
            
            # U_id of the sender
            'sender_id' : int(u_id),
            
            # Actual string of message
            'message' : 'string',
            
            # Import time function
            'time_sent' : time(???)
        }
    ]
}


# members is a list of owners + normal_member ids
# name is the DM name, automatically generated
dm_details_return = {
    'name' :
    'members' : 
}


# DM Create Tests

# Given correct u_ids, return the correct dm_id
def dm_create_v1_succesful_test():
    
    # TODO 
    # Fix tokens creation
    other.clear_v1() 
    auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    auth.auth_register_v2("second@gmail.com", "password", "first", "last")
    auth.auth_register_v2("third@gmail.com", "password", "first", "last")
    auth.auth_register_v2("fourth@gmail.com", "password", "first", "last")

    

    # Owner is 1
    assert(dm.dm_create_v1("TOKEN_ONE", [2,3,4])) == {'dm_id' : 1}
    # Owner is 2
    assert(dm.dm_create_v1("TOKEN_TWO", [1,3,4])) == {'dm_id' : 2}
    # Owner is 3
    assert(dm.dm_create_v1("TOKEN_THREE", [2,4])) == {'dm_id' : 3}
    
# Test any of the u_id in u_ids has not been registered yet
def dm_create_v1_false_member_test():
    other.clear_v1() 
    
    auth.auth_register_v2("first@gmail.com", "password", "first", "last")
   
    with pytest.raises(InputError):
        assert(dm.dm_create_v1("TOKEN_ONE", [2]))
        assert(dm.dm_create_v1("TOKEN_ONE", [2,3,4]))
        assert(dm.dm_create_v1("TOKEN_ONE", [9999]))

# Test given token does not correlate to a real user
def dm_create_v1_false_owner_test():
    other.clear_v1() 
    
    auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    auth.auth_register_v2("second@gmail.com", "password", "first", "last")
    auth.auth_register_v2("third@gmail.com", "password", "first", "last")
    with pytest.raises(InputError):
        assert(dm.dm_create_v1("FALSE TOKEN", [2]))
        
    
# Test duplicate u_ids in the passed-in u_ids list
def dm_create_v1_duplicate_test():
    other.clear_v1() 
    
# Test u_ids list is completely empty
def dm_create_v1_empty_list_test():
    other.clear_v1() 
    
    # Assumption: DM just with the owner
    





