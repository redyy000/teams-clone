import pytest
from src.error import InputError, AccessError
from src import dm
from src import other
from src import auth
'''
InputError when any of:
    dm_id does not refer to a valid DM
    length of message is less than 1 or over 1000 characters
    
AccessError when:
    
    dm_id is valid and the authorised user is not a member of the DM
'''


def invalid_dm_id_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    token_id1 = user_one_info['token']
    u_id2 = user_two_info['auth_user_id']
    u_id3 = user_three_info['auth_user_id']
    dm.dm_create_v1(user_one_info['token'], [u_id2, u_id3])['dm_id']

    dm_id_two = 99999

    with pytest.raises(InputError):
        dm.message_senddm_v1(token_id1, dm_id_two, "Hello World")


def negative_dm_id_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    token_id1 = user_one_info['token']
    u_id2 = user_two_info['auth_user_id']
    u_id3 = user_three_info['auth_user_id']
    dm.dm_create_v1(user_one_info['token'], [u_id2, u_id3])['dm_id']

    with pytest.raises(InputError):
        dm.message_senddm_v1(token_id1, -1, "Hello World")


def invalid_large_message_length_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    token_id1 = user_one_info['token']
    u_id2 = user_two_info['auth_user_id']
    u_id3 = user_three_info['auth_user_id']
    dm_id_1 = dm.dm_create_v1(token_id1, [u_id2, u_id3])['dm_id']

    with pytest.raises(InputError):
        dm.message_senddm_v1(user_one_info, dm_id_1, "a" * 1200)


def invalid_large_message_length_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    token_id1 = user_one_info['token']
    u_id2 = user_two_info['auth_user_id']
    u_id3 = user_three_info['auth_user_id']
    dm_id_1 = dm.dm_create_v1(token_id1, [u_id2, u_id3])['dm_id']

    with pytest.raises(InputError):
        dm.message_senddm_v1(token_id1, dm_id_1, "")


def invalid_auth_user_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    token_id1 = user_one_info['token']
    token_id3 = user_three_info['token']
    u_id2 = user_two_info['auth_user_id']
    u_id3 = user_three_info['auth_user_id']
    dm_id_1 = dm.dm_create_v1(token_id1, [u_id2])['dm_id']

    with pytest.raises(AccessError):
        dm.message_senddm_v1(token_id3, dm_id_1, "Hello World")
