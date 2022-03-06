'''
   Given a channel_id of a channel that the authorised user can join, adds them to that channel.

   Tests to write

   * Channel id does not refer to a valid channel
   * Channel id does not refer to a valid user
   * Channel id refers to a user that is already a member

   * An error occurs when channel id is valid and the authorised user is not a member of the channel. 
   (invite created from person outside of the channel)
   (with pytest.raises(AccessError) - insert tests here)
   '''
import pytest
from src.channel import channel_join_v1, channel_invite_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1, channels_list_v1


# Channel id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    channel_id1 = channels_create_v1(user_id1["auth_user_id"], "general", False)
    channel_id2 = 99999

    with pytest.raises(InputError):
        # Channel 2 does not exist
        assert channel_invite_v1(user_id1["auth_user_id"], channel_id2, user_id2["auth_user_id"])

# An invalid user is invited to join a channel
def test_invalid_uid():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    # user_id2 = auth_register_v1("ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    # Not a real user
    user_id2 = 2
    channel_id1 = channels_create_v1(user_id1["auth_user_id"], "general", False)

    with pytest.raises(InputError):
        # Ryan doesnt exist
        assert channel_invite_v1(user_id1["auth_user_id"], channel_id1["channel_id"], user_id2)

# The invited member is already in the channel


def test_already_a_member():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    channel_id1 = channels_create_v1(user_id1["auth_user_id"], "general", True)
    channel_join_v1(user_id2["auth_user_id"], channel_id1["channel_id"])

    with pytest.raises(InputError):
        # Ryan is alrady a member of the channel
        assert channel_invite_v1(user_id1["auth_user_id"], channel_id1["channel_id"], user_id2["auth_user_id"])


# An unauthorised user invites another user to a channel
def test_unauthorised():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    user_id3 = auth_register_v1(
        "richard@gmail.com", "weakpw", "Richard", "Xue")
    channel_id1 = channels_create_v1(user_id1["auth_user_id"], "general", True)

    with pytest.raises(AccessError):
        # Ryan does not have permissions to invite Richard
        assert channel_invite_v1(user_id2["auth_user_id"], channel_id1["channel_id"], user_id3["auth_user_id"])

# Tests that give valid inputs.

def test_successful_invite():
    clear_v1()
    user_id1 = auth_register_v1("dlin@gmail.com", "password", "Daniel", "Lin")
    user_id2 = auth_register_v1(
        "ryan@gmail.com", "strongpw", "Ryan", "Godakanda")
    user_id3 = auth_register_v1(
        "richard@gmail.com", "weakpw", "Richard", "Xue")
    channel_id1 = channels_create_v1(user_id1["auth_user_id"], "general", True)

    # User should be successfully added to the channel
    channel_invite_v1(user_id1["auth_user_id"], channel_id1["channel_id"], user_id2["auth_user_id"])
    channel_invite_v1(user_id1["auth_user_id"], channel_id1["channel_id"], user_id3["auth_user_id"])

    assert channels_list_v1(user_id2["auth_user_id"]) == {'channels': [
        {"channel_id": channel_id1["channel_id"], "name": "general"}]}
    assert channels_list_v1(user_id3["auth_user_id"]) == {'channels': [
        {"channel_id": channel_id1["channel_id"], "name": "general"}]}