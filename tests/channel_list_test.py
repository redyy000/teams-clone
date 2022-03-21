import pytest
from src.auth import auth_register_v1
from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.channels import channels_create_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.channel import channel_invite_v1

def test_channels_list1():
    #short channels_list test
    clear_v1()
    user_id1 = auth_register_v1('test@gmail.com', '123password', 'John', 'Doe')
    user_id2 = auth_register_v1('anothertest@gmail.com', 'securepassword', 'Jane', 'Doe')
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], 'test_channel', True)
    channel_invite_v1(user_id1['auth_user_id'], channel_id1['channel_id'], user_id2['auth_user_id'])
    assert channels_list_v1(user_id1['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'test_channel'}]}
    assert channels_list_v1(user_id2['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'test_channel'}]}


def test_channels_list2():
    #long channels_list test
    clear_v1()
    user_id1 = auth_register_v1('test123@gmail.com', '123password', 'Jonathan', 'Doe')
    user_id2 = auth_register_v1('anothertest@gmail.com', 'securepassword', 'Jane', 'Doe')
    user_id3 = auth_register_v1('realemail@gmail.com', 'safepassword', 'Jeremy', 'Doe')
    user_id4 = auth_register_v1('real123@gmail.com', 'goodpassword', 'John', 'Smith')
    user_id5 = auth_register_v1('throwaway@gmail.com', 'strongpassword', 'Joanne', 'Citizen')
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], 'General', True)
    channel_id2 = channels_create_v1(user_id1['auth_user_id'], 'Hidden', False)
    channel_id3 = channels_create_v1(user_id4['auth_user_id'], 'John and Joanne', True)
    channel_id4 = channels_create_v1(user_id4['auth_user_id'], 'John PRIVATE', False)
    channel_invite_v1(user_id1['auth_user_id'], channel_id2['channel_id'], user_id2['auth_user_id'])
    channel_invite_v1(user_id2['auth_user_id'], channel_id2['channel_id'], user_id4['auth_user_id'])
    channel_invite_v1(user_id4['auth_user_id'], channel_id3['channel_id'], user_id5['auth_user_id'])
    assert channels_list_v1(user_id1['auth_user_id']) == {'channels': [{'channel_id': channel_id1['channel_id'], 'name': 'General'}, {'channel_id': channel_id2['channel_id'], 'name': 'Hidden'}]}
    assert channels_list_v1(user_id2['auth_user_id']) == {'channels': [{'channel_id': channel_id2['channel_id'], 'name': 'Hidden'}]}
    assert channels_list_v1(user_id3['auth_user_id']) == {'channels': []}
    assert channels_list_v1(user_id4['auth_user_id']) == {'channels': [{'channel_id': channel_id2['channel_id'], 'name': 'Hidden'}, {'channel_id': channel_id3['channel_id'], 'name': 'John and Joanne'}, {'channel_id': channel_id4['channel_id'], 'name': 'John PRIVATE'}]}
    assert channels_list_v1(user_id5['auth_user_id']) == {'channels': [{'channel_id': channel_id3['channel_id'], 'name': 'John and Joanne'}]}

def test_channels_list3():
    #tests invalid user ID
    clear_v1()
    user_id1 = auth_register_v1('test123@gmail.com', '123password', 'Jonathan', 'Doe')
    with pytest.raises(AccessError):
        assert channels_list_v1(3)

def test_channels_listall1():
    #short channels_listall test
    clear_v1()
    user_id1 = auth_register_v1('test@gmail.com', '123password', 'John', 'Doe')
    user_id2 = auth_register_v1('anothertest@gmail.com', 'securepassword', 'Jane', 'Doe')
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], 'test_channel', True)
    channel_invite_v1(user_id1['auth_user_id'], channel_id1['channel_id'], user_id2['auth_user_id'])
    assert channels_listall_v1(user_id2['auth_user_id']) == {'channels': [{'channel_id': channel_id1['channel_id'], 'name': 'test_channel'}]}

def test_channels_listall2():
    #long channels_listall test
    clear_v1()
    user_id1 = auth_register_v1('test123@gmail.com', '123password', 'Jonathan', 'Doe')
    user_id2 = auth_register_v1('anothertest@gmail.com', 'securepassword', 'Jane', 'Doe')
    user_id4 = auth_register_v1('real123@gmail.com', 'goodpassword', 'John', 'Smith')
    user_id5 = auth_register_v1('throwaway@gmail.com', 'strongpassword', 'Joanne', 'Citizen')
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], 'General', True)
    channel_id2 = channels_create_v1(user_id1['auth_user_id'], 'Hidden', False)
    channel_id3 = channels_create_v1(user_id4['auth_user_id'], 'John and Joanne', True)
    channel_id4 = channels_create_v1(user_id4['auth_user_id'], 'John PRIVATE', False)
    channel_invite_v1(user_id1['auth_user_id'], channel_id2['channel_id'], user_id2['auth_user_id'])
    channel_invite_v1(user_id2['auth_user_id'], channel_id2['channel_id'], user_id4['auth_user_id'])
    channel_invite_v1(user_id4['auth_user_id'], channel_id3['channel_id'], user_id5['auth_user_id'])
    assert channels_listall_v1(user_id1['auth_user_id']) == {'channels': [{'channel_id': channel_id1['channel_id'], 'name': 'General'}, {'channel_id': channel_id2['channel_id'], 'name': 'Hidden'}, {'channel_id': channel_id3['channel_id'], 'name': 'John and Joanne'}, {'channel_id': channel_id4['channel_id'], 'name': 'John PRIVATE'}]}

def test_channels_listall3():
    #tests invalid user ID
    clear_v1()
    user_id1 = auth_register_v1('test123@gmail.com', '123password', 'Jonathan', 'Doe')
    with pytest.raises(AccessError):
        assert channels_listall_v1(3)

def test_channels_listall4():
    #tests for 0 channels
    clear_v1()
    user_id1 = auth_register_v1('test123@gmail.com', '123password', 'Jonathan', 'Doe')
    assert channels_listall_v1(user_id1['auth_user_id']) == {'channels': []}
