import pytest
import requests
from src import config

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


def users_all_success_test():
    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")
    user_three_info = auth.auth_register_v2(
        "third@gmail.com", "password", "first", "last")

    users_list = {
        'users': [
            user.user_profile_v1(
                user_one_info['token'], user_one_info['auth_user_id'])['user'],
            user.user_profile_v1(
                user_two_info['token'], user_two_info['auth_user_id'])['user'],
            user.user_profile_v1(
                user_three_info['token'], user_three_info['auth_user_id'])['user']
        ]
    }

    assert(users.users_all_v1(user_one_info['token'])) == users_list


def users_all_remove_test():

    other.clear_v1()
    user_one_info = auth.auth_register_v2(
        "first@gmail.com", "password", "first", "last")
    user_two_info = auth.auth_register_v2(
        "second@gmail.com", "password", "first", "last")

    users_list = {
        'users': [
            user.user_profile_v1(
                user_one_info['token'], user_one_info['auth_user_id'])['user'],
            user.user_profile_v1(
                user_two_info['token'], user_two_info['auth_user_id'])['user'],
        ]
    }

    assert(users.users_all_v1(user_one_info['token'])) == users_list

    # TODO
    # Figure out what an admin is, and write a test where the admin removes
    # User two

    new_users_list = {
        'users': [
            user.user_profile_v1(
                user_one_info['token'], user_one_info['auth_user_id'])['user'],
        ]
    }

    assert(users.users_all_v1(user_one_info['token'])) == new_users_list
