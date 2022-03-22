import datetime
from re import L
from src.error import InputError, AccessError
from src.other import token_create, is_valid_token, load_data, store_data
'''
dm_data_structure = {
    # Name of dm automatically generated
    'name' : 'string',

    # dm id
    'dm_id' : number

    # List of normal member u_ids
    # Normal members == NOT owners
    'normal_members' : [],


    # List of owner u_ids
    # Original creator is first
    'owner' : [],

    # List of message dictionaries
    'messages' : [
        {

            # Message id is now the global message id
            'message_id' : int,

            # U_id of the sender
            'sender_id' : int(u_id),

            # Actual string of message
            'message' : 'string',

            # Time sent
            'time_sent' : datetime.datetime.now()
        }
    ]
}
'''


def dm_name_generate(u_ids):
    '''
    Givven a list of user u_ids,
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
    datastore = load_data()
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

    datastore = load_data()
    # Generate the name of the dm.
    owner_id = token_decoded['u_id']
    all_member_id_list = u_ids
    all_member_id_list.append(owner_id)

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
        # Can we have multiple owners of a DM?
        # Don't think so
        'owner': owner_id,
        'normal_members': u_ids,
        'all_members': all_member_id_list,
        'messages': []
    }

    datastore['dms'].append(dm)
    store_data(datastore)
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
    datastore = load_data()

    dm_list = []
    for dm in datastore['dms']:
        if user_id in dm['all_members']:
            print(dm['name'])
            dm_list.append({
                'dm_id': dm['dm_id'],
                'name': dm['name']
            })

    return {
        'dms': dm_list
    }


def dm_remove_v1():
    pass


def dm_details_v1():
    pass


def message_senddm_v1():
    pass


def dm_leave_v1():
    pass
