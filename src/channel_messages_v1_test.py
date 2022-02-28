from src.channel import channel_messages_v1
from src.channel import channel_details_v1
from src.channel import channel_join_v1
from src.data_store import data_store

##function prototype
##def channel_messages_v1(auth_user_id, channel_id, start):


##test channel_id does not refer to valid channel
def test_channel_id_invalid():
    with pytest.raises(InputError):

##test channel start is greater than total number of messages in channel
def test_channel_index_invalid():
    with pytest.raises(InputError):
        channel_messages_v1("normal@gmail.com", {"auth_user_id": ["normal@gmail.com"], "messages": ["hello"]}, 70)
        channel_messages_v1("normal@gmail.com", {"auth_user_id": ["normal@gmail.com"], "messages": ["hello", "goodbye"] }, 10)
        channel_messages_v1("normal@gmail.com", {"auth_user_id": ["normal@gmail.com"], "messages": []}, -20 )

##test when user is not member of channel
def channel_member_invalid():
    with pytest.raises(AccessError):
        channel_messages_v1("empty@gmail.com", {"auth_user_id": ["normal@gmail.com"], "messages": ["hello"]}, 0)
        channel_messages_v1("test@gmail.com", {"auth_user_id": ["max@gmail.com", "richard@gmail.com", "tayla@gmail.com", "daniel@gmail.com", "ryan@gmail.com"], "messages": ["hello"]}, 0)
