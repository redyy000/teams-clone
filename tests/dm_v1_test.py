from src import auth
from src.error import InputError, AccessError
from src import dm
from src import other
from src import message
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

'''dm_data_structure = {
    # Name of dm automatically generated
    'name': 'string',


    # List of normal member u_ids
    # Normal members == NOT owners
    'normal_members': [],


    # List of owner u_ids
    # Original creator is first
    'owner': [],

    # List of message dictionaries
    'messages': [
        {

            # Messages_id is index of message list + 1
            # I.e. message_id of 1 is message_list[0]
            # message_id of 2 is message_list[1]
            'message_id': int,

            # U_id of the sender
            'sender_id': int(u_id),

            # Actual string of message
            'message': 'string',

            # Import time function
            'time_sent': float(???)
        }
    ]
}


# members is a list of owners + normal_member ids
# name is the DM name, automatically generated
dm_details_return = {
=======
    'name' :
    'members' : 
}
'''

# DM Create Tests
# NOT HTTP TESTS

# Given correct u_ids, return the correct dm_id
def dm_create_v1_succesful_test():

    # TODO
    # Fix tokens creation
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']
    token_four = auth.auth_register_v2(
        "fourth@gmail.com", "password", "first", "last")['token']

    # Owner is 1
    assert(dm.dm_create_v1(token_one, [2, 3, 4])) == {'dm_id': 1}
    # Owner is 2
    assert(dm.dm_create_v1(token_two, [1, 3, 4])) == {'dm_id': 2}
    # Owner is 3
    assert(dm.dm_create_v1(token_three, [2, 4])) == {'dm_id': 3}

# Test any of the u_id in u_ids has not been registered yet


def dm_create_v1_false_member_test():
    other.clear_v1()

    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']

    with pytest.raises(InputError):
        assert(dm.dm_create_v1(token_one, [2]))
        assert(dm.dm_create_v1(token_one, [2, 3, 4]))
        assert(dm.dm_create_v1(token_one, [9999]))

# Test given token does not correlate to a real user


def dm_create_v1_false_owner_test():
    other.clear_v1()

    auth.auth_register_v2("first@gmail.com", "password", "first", "last")
    auth.auth_register_v2("second@gmail.com", "password", "first", "last")
    auth.auth_register_v2("third@gmail.com", "password", "first", "last")
    with pytest.raises(InputError):
        assert(dm.dm_create_v1("FALSE TOKEN", [2, 3]))
        assert(dm.dm_create_v1("FALSE TOKEN", [3]))

# Test when owner is in the u_id list


def dm_create_v1_owner_is_member_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    with pytest.raises(InputError):
        assert(dm.dm_create_v1(token_one, [1]))
        assert(dm.dm_create_v1(token_one, [1, 2]))
        assert(dm.dm_create_v1(token_one, [1, 2, 3]))

# Test duplicate u_ids in the passed-in u_ids list


def dm_create_v1_duplicate_test():
    other.clear_v1()

    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    with pytest.raises(InputError):
        assert(dm.dm_create_v1(token_one, [2, 2, 2]))
        assert(dm.dm_create_v1(token_one, [2, 3, 3]))
        assert(dm.dm_create_v1(token_one, [2, 3, 2, 3]))


# Test u_ids list is completely empty
def dm_create_v1_empty_list_test():
    other.clear_v1()

    # TODO
    # Use dm_details

    # Assumption: Creates a DM just with the owner

    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']

    assert(dm.dm_create_v1(token_one, [])) == {'dm_id': 1}

    # dm_details to check only user is owner

    assert()

# DM details tests

# Test success


def dm_details_v1_success_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2, 3])['dm_id']


    dm_details_one = {
        'name' : 'aa, bb, cc',
        'members' : [1,2,3]
    }
    assert(dm.dm_details_v1(token_one, dm_id_one)) == dm_details_one

    dm_id_two = dm.dm_create_v1(token_two, [1, 3])['dm_id']

    dm_details_two = {
        'name' : 'aa, bb, cc',
        'members' : [1,2,3]
    }

    assert(dm.dm_details_v1(token_one, dm_id_one)) == dm_details_two

# Test dm_id does not exist


def dm_details_v1_false_id_test():

    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2, 3])
    dm_id_two = 9999

    with pytest.raises(InputError):
        dm.dm_details_v1(token_one, dm_id_two)

  # Test dm_id exists but authorised user is not a member of the DM


def dm_details_v1_unauthorised_user_test():
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2])

    with pytest.raises(AccessError):
        dm.dm_details_v1(token_three, dm_id_one)

# Tests case in which dm_id refers to an invalid DM
def dm_remove_v1_invalid_id_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    dm_details_two = {
        'name' : 'aa, bb, cc',
        'members' : [1,2,3]
    }
    with pytest.raises(InputError):
        dm.dm_remove_v1(token_one, {'dm_id' : 2})

# Tests case in which authorised user is not the original DM creator
def dm_remove_v1_invalid_creator_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    with pytest.raises(AccessError):
        dm.dm_remove_v1(token_two, {'dm_id' : 1})

# Tests case in which the creator of the DM has already left
def dm_remove_v1_missing_creator_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    dm.dm_leave_v1(token_one, {'dm_id' : 1})
    with pytest.raises(AccessError):
        dm.dm_remove_v1(token_one, {'dm_id' : 1})

# Tests case where DM is removed succesfully
def dm_remove_v1_succesful_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    dm.dm_remove_v1(token_one, {'dm_id' : 1})

# Tests general case of dm_list_v1
def dm_list_v1_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    dm_id_two = dm.dm_create_v1(token_two, [3])['dm_id']
    assert dm_list_v1(token_one) == {'dms': [{'name': 'aa, bb, cc', 'members': [1,2,3]}]}
    assert dm_list_v1(token_two) == {'dms': [{'name': 'aa bb, cc', 'members': [1,2,3]}, {'name': 'bb, cc', 'members': [2,3]}]}
    assert dm_list_v1(token_three) == {'dms': [{'name': 'aa, bb, cc', 'members': [1,2,3]}, {'name': 'bb, cc', 'members': [2,3]}]}

# Tests list where a member has left a channel
def dm_list_v1_user_left_test():
    other.clear_v1()
    token_one = auth.auth_register_v2("first@gmail.com", "password", "A", "a")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "B", "b")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "C", "c")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    dm_id_two = dm.dm_create_v1(token_two, [3])['dm_id']
    dm.dm_leave_v1(token_one, dm_id_one)
    assert dm_list_v1(token_one) == {'dms': []}
    assert dm_list_v1(token_two) == {'dms': [{'name': 'aa bb, cc', 'members': [1,2,3]}, {'name': 'bb, cc', 'members': [2,3]}]}
    assert dm_list_v1(token_three) == {'dms': [{'name': 'aa, bb, cc', 'members': [1,2,3]}, {'name': 'bb, cc', 'members': [2,3]}]}

# Assumptions:

# Given a DM id, the user is removed
# Creator is allowed to leave, DM is NOT deleted
    # Owners will just be empty
# DM name remains unchanged

# Test a member successfully leaves
def dm_leave_v1_successful_member_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2, 3])['dm_id']

    dm_leave_v1(token_two, dm_id_one)

    # Member 2 having left
    dm_details_one = {
        'name' : 'aa, bb, cc',
        'members' : [1,3]
    }

    assert(dm_details_v1(token_one, dm_id_one) == dm_details_one)

# Test an owner successfully leaves


def dm_leave_v1_successful_owner_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2, 3])['dm_id']

    dm_leave_v1(token_one, dm_id_one)

    # Owner 1 having left
    dm_details_one = {
        'name' : 'aa, bb, cc',
        'members' : [2,3]
    }

    assert(dm_details_v1(token_two, dm_id_one) == dm_details_one)

# Test dm_id does not exist


def dm_leave_v1_false_id_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    dm_id_false = 999999

    with pytest.raises(InputError):
        assert(dm_leave_v1(token_one, dm_id_false))


# Test dm_id is valid but token user is NOT a DM member

def dm_leave_v1_unauthorised_user_test():
    other.clear_v1()
    token_one = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")['token']

    dm_id_one = dm.dm_create_v1(token_one, [2])['dm_id']

    with pytest.raises(AccessError):
        assert(dm_leave_v1(token_three, dm_id_one))
        
        
        
# Test DM Messages

def dm_messages_v1_successful_test():
    
    other.clear_v1() 
    token_one = auth.auth_register_v2("first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "first", "last")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    
    message.message_senddm_v1(token_one, dm_id_one, "First!")
    message.message_senddm_v1(token_two, dm_id_one, "Lame!")
    message.message_senddm_v1(token_one, dm_id_one, "Third....!")
    
    message_return = {
        'messages': ["First!",  "Lame!", "Third....!"],
        'start'   :  0,
        'end'     :  -1
    }
    
    assert(dm_messages_v1(token_one, dm_id_one, 0)) == message_return
    
    
    
# Test pagination, as well as over 50 tests
# Tests 3 calls are made, instead of one really big call
def dm_messages_v1_hundred_twenty_test():
    other.clear_v1() 
    
    token_one = auth.auth_register_v2("first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "first", "last")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    
    
    for spam in range(0,120):
        message.message_senddm_v1(token_one, dm_id_one, "Now this is epic")
        
    # Are these starts and ends right?
    message_return_one = {
        'messages': ["Now this is epic" * 50],
        'start'   :  0,
        'end'     :  50
    }
    
    message_return_one = {
        'messages': ["Now this is epic" * 50],
        'start'   :  50,
        'end'     :  100
    }
    
    message_return_one = {
        'messages': ["Now this is epic" * 50],
        'start'   :  100,
        'end'     :  -1
    }
    
    assert(dm_messages_v1(token_one, dm_id_one, 0)) == message_return_one
    assert(dm_messages_v1(token_one, dm_id_one, 50)) == message_return_two
    assert(dm_messages_v1(token_one, dm_id_one, 100)) == message_return_three

# Invalid dm_id
def dm_messages_v1_dm_false_test():

    other.clear_v1() 
    token_one = auth.auth_register_v2("first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "first", "last")['token']
    dm_id_two = 9999
    
    with pytest.raises(InputError):
        assert(dm.dm_messages_v1(token_one, dm_id_two, 0))
       
    
# Invalid start; greater than the total amount of messages
def dm_messages_v1_start_too_great_test():
    
    other.clear_v1() 
    token_one = auth.auth_register_v2("first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "first", "last")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2,3])['dm_id']
    
    for spam in range(0,37):
        message.message_senddm_v1(token_one, dm_id_one, "Spam")
    
    with pytest.raises(InputError):
        assert(dm.dm_messages_v1(token_one, dm_id_one, 45))
       
    
def dm_messages_v1_unauthorised_user_test():
    other.clear_v1() 
    token_one = auth.auth_register_v2("first@gmail.com", "password", "first", "last")['token']
    token_two = auth.auth_register_v2("second@gmail.com", "password", "first", "last")['token']
    token_three = auth.auth_register_v2("third@gmail.com", "password", "first", "last")['token']
    dm_id_one = dm.dm_create_v1(token_one, [2])['dm_id']
    
    with pytest.raises(AccessError):
        assert(dm.dm_messages_v1(token_three, dm_id_one, 0))