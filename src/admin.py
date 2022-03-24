
from src.error import InputError, AccessError
from src.other import is_valid_token, load_data, store_data


def is_u_id_exist(u_id):
    '''
    Given u_id
    Return True if u_id is a valid user
    Else return False
    Arguments:
        u_id, (int), u_id to be checked

    Exceptions:
        N/A

    Return Value:
        True/False
    '''

    datastore = load_data()
    for user in datastore['users']:
        if user['u_id'] == u_id:
            return True

    return False


def is_u_id_final_global_owner(u_id):
    '''
    Given u_id
    Return True if u_id is the ONLY global owner
    Else return False
    Arguments:
        u_id, (int), u_id to be checked

    Exceptions:
        N/A

    Return Value:
        True/False
    '''

    datastore = load_data()
    owners_list = [user['u_id']
                   for user in datastore['users'] if user['permission_id'] == 1]
    if len(owners_list) == 1:
        if owners_list[0] == u_id:
            return True

    return False


def is_global_owner(u_id):
    '''
    Given u_id 
    Return True if u_id is a global owner
    Else return False
    Arguments:
        u_id, (int), u_id to be checked
    Exceptions:
        N/A

    Return Value:
        True/False
    '''

    datastore = load_data()
    for user in datastore['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True

    return False


def is_permission_same(u_id, permission_id):
    '''
    Given u_id, permission_id 
    If permission_id of user is already the same as permission_id
    Return true
    Else return false
    Arguments:
        u_id, (int), u_id to be checked
        permission_id (int), permission_id to be checked
    Exceptions:
        N/A

    Return Value:
        True/False
    '''

    datastore = load_data()
    for user in datastore['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == permission_id:
                return True

    return False


def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a global owner's token, u_id and permission_id
    Change the u_id user's permissions to permission_id
    Arguments:
        token, (token), given user token 
        u_id, (int), user whose permission is to be changed
        permission_id (int), permission_id of which the user's permission is to be changed to

    Exceptions:
        InputError - Given u_id does not exist
        InputError - Given u_id is the ONLY global owner left, and they are being demoted to a user
        InputError - Invalid permission_id
        InputError - u_id's permission are already permission_id

        AccessError - Authorised user is not a global owner.
        AccessError - Incorrect token

    Return Value:
        {}
    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = load_data()
    owner_id = token_decoded['u_id']

    if is_u_id_exist(u_id) == False:
        raise InputError(description='Non-existant u_id given!')

    if is_global_owner(owner_id) == False:
        raise AccessError(description="You're not a global owner, forbidden!")

    if is_u_id_final_global_owner(u_id) == True:
        raise InputError(description='u_id is the final global owner!')

    if permission_id < 1 or permission_id > 2:
        raise InputError(description='Invalid permission_id')

    if is_permission_same(u_id, permission_id) == True:
        raise InputError(description='Already the same permission_id')

    for user in datastore['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id

    store_data(datastore)
    return {}


def admin_user_remove_v1(token, u_id):

    pass
