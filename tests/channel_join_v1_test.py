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
from src.channels import channels_create_v1


# Tests for invalid channel

def invalid_channel_id_test():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    channel_id1 = channels_create_v1(user_id1, "general", 1)

    with pytest.raises(InputError):
        # Only channel 1 is created, channel 2 does not exist
        assert channel_join_v1(user_id1, channel_id2)


# Test for already joined channel
def already_joined_test():

    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    channel_id1 = channels_create_v1(user_id1, "general", 1)

    with pytest.raises(InputError):
        # Creating the channel auto joins the person
        assert channel_join_v1(user_id1, channel_id1)

# Test for attempt to join priv channel


def private_channel_test():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    channel_id1 = channels_create_v1(user_id1, "general", 0)

    with pytest.raises(AccessError):
        # Ryan cannot join the private server
        assert channel_join_v1(user_id2, channel_id1)

