import py
import pytest

from src.data_store import data_store
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError


store = data_store.get


def test_successful():
    clear_v1()
    # test that member of channel can access channel details, as well as owner
    owner = auth_register_v1('channelowner@gmail.com',
                             'testpassword1', 'first', 'last')
    user1 = auth_register_v1(
        'user1@gmail.com', 'testpassword', 'firstname', 'lastname')
    new_channel1 = channels_create_v1(
        owner['auth_user_id'], 'New Channel 1', True)
    # joins user1 to channel
    channel_join_v1(user1['auth_user_id'], new_channel1['channel_id'])
    assert owner['auth_user_id'] == 1
    assert user1['auth_user_id'] == 2
    assert new_channel1['channel_id'] == 1

    assert channel_details_v1(user1['auth_user_id'], new_channel1['channel_id']) == {  # asserts details are updated after join, member has access
        'name': 'New Channel 1',
        'is_public': True,
        'owner_members': [{
            'u_id': owner['auth_user_id'],
            'email':'channelowner@gmail.com',
            'name_first':'first',
            'name_last':'last',
            'handle_str':'firstlast'
        }],
        'all_members': [{
            'u_id': owner['auth_user_id'],
            "email":'channelowner@gmail.com',
            'name_first': 'first',
            'name_last':'last',
            'handle_str':'firstlast'
        },
            {
            'u_id': user1['auth_user_id'],
            'email':'user1@gmail.com',
            'name_first':'firstname',
            'name_last':'lastname',
            'handle_str':'firstnamelastname'
        }],
    }
    assert channel_details_v1(owner['auth_user_id'], new_channel1['channel_id']) == {  # asserts owner has access to details
        'name': 'New Channel 1',
        'is_public': True,
        'owner_members': [{
            'u_id': owner['auth_user_id'],
            'email':'channelowner@gmail.com',
            'name_first':'first',
            'name_last':'last',
            'handle_str':'firstlast',
        }, ],
        'all_members': [{
            'u_id': owner['auth_user_id'],
            "email":'channelowner@gmail.com',
            'name_first': 'first',
            'name_last':'last',
            'handle_str':'firstlast',
        },
            {
            'u_id': user1['auth_user_id'],
            'email':'user1@gmail.com',
            'name_first':'firstname',
            'name_last':'lastname',
            'handle_str':'firstnamelastname',
        }, ],
    }


def test_invalid_channel_id():  # PASSED 8:33
    clear_v1()
    # creates 2 test channels
    validuser1 = auth_register_v1(
        'user1@gmail.com', 'testpassword1', 'first', 'last')
    validuser2 = auth_register_v1(
        'user2@gmail.com', 'testpassword2', 'first2', 'last2')
    channels_create_v1(validuser1['auth_user_id'], 'user1', True)
    channels_create_v1(validuser2['auth_user_id'], 'user2', True)
    # asserts channel_ids <1 and > len(store['channels']) are invalid
    with pytest.raises(InputError):
        assert channel_details_v1(validuser1['auth_user_id'], -1)
        assert channel_details_v1(validuser2['auth_user_id'], 7)


def test_non_member():  # Assuming a valid auth_user_id and channel_id
    clear_v1()
    member_user = auth_register_v1(
        'member@gmail.com', 'testpasswordmem', 'firstmem', 'lastmem')
    non_member_user = auth_register_v1(
        'nonmember@gmail.com', 'testpasswordnon', 'firstnon', 'lastnon')
    channel_id1 = channels_create_v1(
        member_user['auth_user_id'], 'Test Channel 1', True)
    with pytest.raises(AccessError):
        assert channel_details_v1(
            non_member_user['auth_user_id'], channel_id1['channel_id'])

        # assert channel_details_v1(10, channel_id1['channel_id'])
        # assert channel_details_v1(0, channel_id1['channel_id'])
        # assert channel_details_v1(-1, channel_id1['channel_id'])
        # assert channel_details_v1(len(store['users']+1), channel_id1)


def test_invalid_auth_user_id():  # PASSED 8:25 // not passed when commenting out invalid Id from create
    with pytest.raises(AccessError):
        clear_v1()
        test_user = auth_register_v1(
            'testuser@gmail.com', 'testpassword5', 'first5', 'last5')
        channel_id2 = channels_create_v1(
            test_user["auth_user_id"], "Test Channel2", True)
    # tests auth_user_id is valid
        assert channel_details_v1(10, channel_id2["channel_id"])
        assert channel_details_v1(0, channel_id2["channel_id"])
        assert channel_details_v1(-1, channel_id2["channel_id"])
