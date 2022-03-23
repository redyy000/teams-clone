'''
Given a channel_id of a channel that the authorised user can join, adds them to that channel.

Tests to write
InputError when
* Channel_id does not refer to a valid channel
* The authorised user is already a member of the channel

AccessError when
Channel_id refers to a channel that is private and the user is not already a channel member, nor are they a global owner.
'''

import pytest
from src.channel import channel_join_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1, channels_list_v1


# Tests for invalid channel

def test_invalid_channel_id():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], "general", True)
    channel_id2 = 99999

    with pytest.raises(InputError):
        # Only channel 1 is created, channel 2 does not exist
        channel_join_v1(user_id1['auth_user_id'], channel_id2)


# Test for already joined channel
def test_already_joined():

    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], "general", True)

    with pytest.raises(InputError):
        # Creating the channel auto joins the person
        channel_join_v1(user_id1['auth_user_id'], channel_id1['channel_id'])

# Test for attempt to join priv channel


def test_private_channel():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    channel_id1 = channels_create_v1(
        user_id1['auth_user_id'], "secret", False)

    with pytest.raises(AccessError):
        # Ryan cannot join the private server
        channel_join_v1(user_id2['auth_user_id'], channel_id1['channel_id'])


def test_successful_join():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    user_id3 = auth_register_v1(
        "richard@gmail.com", "weakpw", "Richard", "Xue")
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], "general", True)

    channel_join_v1(user_id2["auth_user_id"], channel_id1['channel_id'])
    channel_join_v1(user_id3["auth_user_id"], channel_id1['channel_id'])

    assert channels_list_v1(user_id2["auth_user_id"]) == {'channels': [
        {"channel_id": channel_id1["channel_id"], "name": "general"}]}
    assert channels_list_v1(user_id3["auth_user_id"]) == {'channels': [
        {"channel_id": channel_id1["channel_id"], "name": "general"}]}
