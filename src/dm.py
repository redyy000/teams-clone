from src.error import InputError, AccessError
from src.other import token_create, is_valid_token
from src.data_store import data_store
from src.user import user_profile_v1
from datetime import timezone
import datetime


def create_time_stamp():
    '''
    Return the current UTC time_stamp
    '''
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp


def dm_name_generate(u_ids):
    '''
    Given a list of user u_ids,
    Make a name for a dm.
    Name should be an alphabetically-sorted, comma-and-space-separated list of user handles
    e.g. 'ahandle1, bhandle2, chandle3'.
    Returns name

    Arguments:
        owner_u_id (int), u_id of the owner
        member_u_id_list (list of ints), a list of member u_ids.

    Exceptions:
        None

    Return Value:
        name (string)
    '''

    # Create a list of user handles
    datastore = data_store.get()
    handle_str_list = [user['handle_str']
                       for user in datastore['users'] if user['u_id'] in u_ids]
    handle_str_list.sort()
    name = ', '.join([handle for handle in handle_str_list])
    #  The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
    return name


def dm_create_v1(token, u_ids):
    '''
    Given an owner token and a list of member u_ids,
    Make a dm with name.
    Return a dm_id
    Arguments:
        Token (token), owner's token
        u_ids (list of ints), a list of members (Does not include owner)

    Exceptions:
        AccessError - Invalid Token
        InputError  - Non-existant u_id
        InputError  - Duplicate 'u_ids' in list u_ids.

    Return Value:
        {
            'dm_id' : dm_id (int)
        }
    '''

    # What happens if owner id is in u_ids?
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    # Generate the name of the dm.
    owner_id = token_decoded['u_id']

    all_member_id_list = u_ids + [owner_id]

    # Check for non-existant u_ids
    existing_u_id_list = [user['u_id'] for user in datastore['users']]
    for u_id in u_ids:
        if u_id not in existing_u_id_list:
            raise InputError(description='Non-existant u_id given!')

    # Check for duplicate ids
    if len(set(all_member_id_list)) != len(all_member_id_list):
        raise InputError(description='Duplicate u_ids in your dms!!!')

    dm_id = len(datastore['dms']) + 1
    dm = {
        'name': dm_name_generate(all_member_id_list),
        'dm_id': dm_id,
        'owners': [owner_id],
        'normal_members': u_ids,
        'all_members': all_member_id_list,
        'messages': []
    }

    # Increase amount of dms for seams stats
    time_stamp = create_time_stamp()
    seams_dm_entry = {
        'num_dms_exist': datastore['workplace_stats']['dms_exist'][-1]['num_dms_exist'] + 1,
        'time_stamp': time_stamp
    }
    datastore['workplace_stats']['dms_exist'].append(seams_dm_entry)

    # Increase amount of dms joined for each member of dm.
    for u_id in all_member_id_list:
        # Increase dms_joined stat for each one....
        # Suspicious usage of u_id to find user index
        user_dm_entry = {
            'num_dms_joined': datastore['users'][u_id - 1]['stats']['dms_joined'][-1]['num_dms_joined'] + 1,
            'time_stamp': time_stamp
        }
        datastore['users'][u_id -
                           1]['stats']['dms_joined'].append(user_dm_entry)

    datastore['dms'].append(dm)
    data_store.set(datastore)
    return {
        'dm_id': dm_id
    }


def dm_list_v1(token):
    '''
    Given a token,
    Return the list of DMs that the token id is a member of.
    Arguments:
        Token (token), user token

    Exceptions:
        AccessError - Invalid Token

    Return Value:

        List of { dm_id, name } dictionaries

    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    user_id = token_decoded['u_id']
    datastore = data_store.get()

    dm_list = []
    for dm in datastore['dms']:
        if user_id in dm['all_members']:
            dm_list.append({
                'dm_id': dm['dm_id'],
                'name': dm['name']
            })

    return {
        'dms': dm_list
    }


def dm_remove_v1(token, dm_id):
    '''
    Given a token and dm_id,
    Remove a DM so that there are no more members.
    Arguments:
        Token (token), user token
        Dm_id (int), id of the dm to be removed

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_id is valid but user is not the owner
        AccessError - dm_is is valid but user is not a member of the dm
        InputError -  dm_id is invalid


    Return Value:

        {}

    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    user_id = token_decoded['u_id']

    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:

            # If user_id is not a member of the dm...
            # All non-owners are obviously not normal members or members at all.
            if user_id not in dm['all_members']:
                raise AccessError(
                    description='User is not a member of the DM!')
            # If user_id is not the owner of the dm...

            if user_id not in dm['owners']:
                raise AccessError(description='User is not the owner!')

            time_stamp = create_time_stamp()

            # Update user stats
            # Increase amount of dms joined for each member of dm.
            for u_id in dm['all_member_id_list']:
                # Increase dms_joined stat for each one....
                # Suspicious usage of u_id to find user index
                user_dm_entry = {
                    'num_dms_joined': datastore['users'][u_id - 1]['stats']['dms_joined'][-1]['num_dms_joined'] - 1,
                    'time_stamp': time_stamp
                }
                datastore['users'][u_id -
                                   1]['stats']['dms_joined'].append(user_dm_entry)

            # DM is fully removed.

            datastore['dms'].remove(dm)

            # Update seams stats
            # Decrease amount of dms for seams stats

            seams_dm_entry = {
                'num_dms_exist': datastore['workplace_stats']['dms_exist'][-1]['num_dms_exist'] - 1,
                'time_stamp': time_stamp
            }
            datastore['workplace_stats']['dms_exist'].append(seams_dm_entry)

            data_store.set(datastore)
            return {}
    # If given dm_id does not exist
    raise InputError(description='Given dm does not exist')


def dm_details_v1(token, dm_id):
    '''
    Given a token and dm_id,
    Return basic information about the DM.
    {name, members}
    Arguments:
        Token (token), user token
        Dm_id (int), id of the dm to be removed

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_is is valid but user is not a member of the dm
        InputError -  dm_id is invalid


    Return Value:

        { name, members }

    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')
    user_id = token_decoded['u_id']

    datastore = data_store.get()

    # Test DM ID Exists
    dm_exist = False
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            dm_exist = True
    if dm_exist == False:
        raise InputError(description='Given dm does not exist')
    dm_name = ''
    members_list = []
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            if user_id not in dm['all_members']:
                raise AccessError(
                    description='User is not a member of the DM!')
            dm_name = dm['name']
            # Grab user details
            for user in dm['all_members']:
                user_dict = user_profile_v1(token, user)['user']
                members_list.append(user_dict)

    return {
        'name': dm_name,
        'members': members_list
    }


def dm_leave_v1(token, dm_id):
    '''
    Given a token and dm_id,
    Make the token's user leave the dm.
    Return {}
    Arguments:
        Token (token), user token
        Dm_id (int), id of the dm to leave from

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_is is valid but user is not a member of the dm
        InputError -  dm_id is invalid

    Return Value:

        {}

    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')
    user_id = token_decoded['u_id']
    datastore = data_store.get()

    # Test DM ID Exists
    dm_exist = False
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            dm_exist = True
    if dm_exist == False:
        raise InputError(description='Given dm does not exist')

    user_exist = False
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            if user_id in dm['all_members']:
                dm['all_members'].remove(user_id)
                user_exist = True
            if user_id in dm['owners']:
                dm['owners'].remove(user_id)
                user_exist = True
            if user_id in dm['normal_members']:
                dm['normal_members'].remove(user_id)
                user_exist = True

            # Update user stats by decreasing
            time_stamp = create_time_stamp()
            user_dm_entry = {
                'num_dms_joined': datastore['users'][user_id - 1]['stats']['dms_joined'][-1]['num_dms_joined'] - 1,
                'time_stamp': time_stamp
            }
            datastore['users'][user_id -
                               1]['stats']['dms_joined'].append(user_dm_entry)
            data_store.set(datastore)

    if user_exist == False:
        raise AccessError(description='DM exists, however user is not in DM')

    return {}


def dm_messages_v1(token, dm_id, start):
    '''
    Given a token, dm_id and start id
    Return up to 50 messages from index start and index start + 50,
    Where 0 is the most recent message.
    Returns a new index which is the value of start + 50, or if the least recent message has been returned,
    Returns - 1.
    Arguments:
        Token(token), user token
        Dm_id(int), id of the dm's whose messages are returned
        start(int), index of which to start sending messages.

    Exceptions:
        AccessError - Invalid Token
        AccessError - dm_is is valid but user is not a member of the dm
        InputError - dm_id is invalid
        InputError - start is higher than total number of messages

    Return Value:

        {messages, start, end}
    '''
    # Invalid token
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    user_id = token_decoded['u_id']
    datastore = data_store.get()

    # Check dm exists
    message_count = -1
    dm_exist = False
    user_exist = False
    for dm in datastore['dms']:
        if dm['dm_id'] == dm_id:
            message_count = len(dm['messages'])
            dm_exist = True
            if user_id in dm['all_members']:
                user_exist = True

    # Check user in dm

    if dm_exist == False:
        raise InputError(description='Dm id does not exist!')
    if user_exist == False:
        raise AccessError(description='Non-authorised user!!!')

    # Check starting id is valid
    if start > message_count or isinstance(start, int) == False or start < 0:
        raise InputError(description='Start index is too high!')

    # Temporary end variable
    end = start + 50

    dm_list = datastore['dms']
    dm_selected = dm_list[dm_id - 1]
    dm_messages = dm_selected['messages']

    message_list = []
    recent_message_list = dm_messages[::-1]

    end_fail = False
    for idx in range(start, start + 50):
        try:
            message_list.append(recent_message_list[idx])
        except:
            end_fail = True
            break
    if end_fail == True:
        end = -1
    else:
        end = start + 50

    return {
        'messages': message_list,
        'start': start,
        'end': end
    }
