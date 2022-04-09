import re
from src.error import InputError, AccessError
from src.other import is_valid_token
from src.data_store import data_store
from datetime import timezone
import datetime
import urllib.request
from PIL import Image


def get_user_from_store(u_id):
    datastore = data_store.get()
    for user in datastore['users']:
        if user['u_id'] == u_id:
            return user


def user_profile_v1(token, u_id):
    '''
    Given a token and a u_id,
    Evaluate the u_id and decode token,
    Then return user dictionary with information:
        user_id, email, first name, last name, and handle


    Arguments:
        token (token), token for authentication
        u_id (int), u_id of user whose info is to be returned

    Exceptions:
        InputError: Given u_id does not exist
        AccessError: Invalid token

    Return Value:
        {
            'u_id'  : u_id,
            'email' : email of u_id,
            'name_first', first name of u_id,
            'name_last', last name of u_id,
            'handle_str', handle of u_id,
            'profile_img_url', profile_pic_url
        }
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    return_dict = {}
    user_found = False
    for user in datastore['users']:
        if user['u_id'] == u_id:
            return_dict = {

                'user': {
                    'u_id': u_id,
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str'],
                    'profile_img_url': user['profile_img_url']
                }
            }
            user_found = True

    if user_found == False:
        raise InputError(description="Non-existant user!")
    return return_dict


def user_profile_setname_v1(token, name_first, name_last):
    '''
    Given a token, name_first and name_last
    Decode and evaluate the token to find authorised user
    Change user's first and last names

    Arguments:
        token (token), token for authentication
        name_first (string), new first name
        name_last  (string), new last name

    Exceptions:
        InputError: name_first not between 1-50 characters inclusive
        InputError: name_last not between 1-50 characters inclusive
        AccessError: Invalid token

    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    if isinstance(name_first, str) == False or isinstance(name_last, str) == False:
        raise InputError(description="First/Last names must be strings!")

    if len(name_first) > 50 or len(name_first) <= 0:
        raise InputError(description="First name length is invalid!")
    elif len(name_last) > 50 or len(name_last) <= 0:
        raise InputError(description="Last name length is invalid!")

    for user in datastore['users']:
        if user['u_id'] == u_id:

            user['name_first'] = name_first
            user['name_last'] = name_last

    data_store.set(datastore)
    return {}


def user_profile_setemail_v1(token, email):
    '''
    Given a token and email
    Decode and evaluate the token to find authorised user
    Change user's email to email
    Handle is not changed

    Arguments:
        token (token), token for authentication
        email (string), new email for user

    Exceptions:
        InputError: Email is an invalid email(REGEX)
        InputError: Email is already being used
        AccessError: Invalid token

    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    # Determine if email matches regular expression.
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if (re.fullmatch(regex, email)) == None:
        raise InputError(
            description="Email does not match the regular expression!")

    # Check for email already existing

    for user in datastore['users']:
        if email == user['email']:
            raise InputError(
                description="Email already exists and is being used!")

    for user in datastore['users']:
        if user['u_id'] == u_id:
            user['email'] = email

    data_store.set(datastore)
    return {}


def user_stats_v1(token):
    '''
    Given a token,
    Return user_stats:
    The number of channels the user is a part of
    The number of DMs the user is a part of
    The number of messages the user has sent
    The user's involvement, as defined by this pseudocode: sum(num_channels_joined, num_dms_joined, num_msgs_sent)/sum(num_channels, num_dms, num_msgs).
    If the denominator is 0, involvement should be 0. If the involvement is greater than 1, it should be capped at 1.

    Arguments:
        token (token), token for authentication

    Exceptions:
        AccessError: Invalid Token

    Return Value:
        { user_stats }
    '''
    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError('False Token!')

    datastore = data_store.get()

    u_id = token_decoded['u_id']

    # Used for calculating user involvement
    # General stats of seams
    num_channels_exist = len(datastore['channels'])
    num_dms_exist = len(datastore['dms'])
    num_messages_exist = 0
    for channel in datastore['channels']:
        num_messages_exist = num_messages_exist + len(channel['messages'])

    for dm in datastore['dms']:
        num_messages_exist = num_messages_exist + len(dm['messages'])

    # User specific stats
    num_channels_joined = 0
    num_dms_joined = 0
    num_msgs_sent = 0

    # Calculating channels joined and channel msgs sent
    for channel in datastore['channels']:
        for member_dict in channel['all_members']:
            if u_id == member_dict['user_id']:
                num_channels_joined = num_channels_joined + 1
                break

        for message_dict in channel['messages']:
            if message_dict['u_id'] == u_id:
                num_msgs_sent = num_msgs_sent + 1

    # Calculating dms joined and dm msgs sent
    for dm in datastore['dms']:
        if u_id in dm['all_members']:
            num_dms_joined = num_dms_joined + 1

        for message_dict in dm['messages']:
            if message_dict['u_id'] == u_id:
                num_msgs_sent = num_msgs_sent + 1

    # Denominator
    denominator = sum([num_channels_exist, num_dms_exist, num_messages_exist])
    if denominator == 0:
        involvement = 0
    else:
        involvement = float(sum([num_channels_joined, num_dms_joined,
                                num_msgs_sent]))/float(denominator)
    if involvement > 1:
        involvement = 1

    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    time_stamp = int(utc_time.timestamp())

    '''As UNSW is very interested in its users' engagement, the analytics must be time-series data. 
    This means every change to the above metrics (excluding involvement_rate and utilization_rate) must be timestamped, rather than just the most recent change. 
    For users, the first data point should be 0 for all metrics at the time that their account was created. 
    Similarly, for the workspace, the first data point should be 0 for all metrics at the time that the first user registers. 
    The first element in each list should be the first metric. The latest metric should be the last element in the list.'''

    stats = {
        'channels_joined': [{'num_channels_joined': num_channels_joined, 'time_stamp': time_stamp}],
        'dms_joined': [{'num_dms_joined': num_dms_joined, 'time_stamp': time_stamp}],
        'messages_sent': [{'num_messsages_sent': num_msgs_sent, 'time_stamp': time_stamp}],
        'involvement_rate': involvement
    }

    return {
        'user_stats': stats

    }


def user_profile_sethandle_v1(token, handle_str):
    '''
    Given a token and handle_str
    Decode and evaluate the token to find authorised user
    Change user's handle to handle_str

    Arguments:
        token (token), token for authentication
        handle_str (string), new handle for user

    Exceptions:
        InputError: handle_str not between 3-20 characters inclusive
        InputError: handle_str contains non-alphanumeric characters
        InputError: handle_str already being used as a handle
        AccessError: Invalid token
    Return Value:
        {}
    '''

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    for user in datastore['users']:
        if handle_str == user['handle_str']:
            raise InputError(
                description="Handle already exists and is being used!")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(
            description="Handle length must be between 3-20 characters inclusive!")
    elif handle_str.isalnum() == False:
        raise InputError(description="Handle must be alphanumeric!")

    for user in datastore['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str

    data_store.set(datastore)

    return {}


def photo_crop(img_file, x_start, y_start, x_end, y_end):
    '''
    Given a img_file
    Crop the image with the given bounds
    Save over original img with new cropped img

    Arguments:
        img_file (string), file in file system for an image to be cropped
        x_start (int), x coordinate start for crop
        y_start (int), y coordinate start for crop
        x_end (int), x coordinate end for crop
        y_end (int), y coordinate end for crop

    Exceptions:
        None
    Return Value:
        None
    '''

    imageObject = Image.open(img_file)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_file)


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    pass
    '''
    Given a token and and a img_url
    Decode and evaluate the token to find authorised user
    Change user's profile_img_url to img_url, 
    Cropped within the given bounds

    Arguments:
        token (token), token for authentication
        img_url (string), url for an image to be used as the new profile picture
        x_start (int), x coordinate start for crop
        y_start (int), y coordinate start for crop
        x_end (int), x coordinate end for crop
        y_end (int), y coordinate end for crop

    Exceptions:
        InputError: img_url returns a non-200 status or any error occurs when retrieving img
        InputError: Any of the x-y starts/ends are not within dimensions of the image
        InputError: x_end < x_start, or y_end < y_start
        InputError: Image uploaded is not a jpg
    Return Value:
        {}
    '''
    # TODO Input Errors
    # Download image

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    if x_end < x_start or y_end < y_start:
        raise InputError(description='Given crop dimensions are invalid!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    # Retrieve handle_str
    user_handle_str = get_user_from_store(u_id)['handle_str']

    img_file = 'src/images/' + user_handle_str + '_profile_pic.jpg'
    # Download image from url, save it to images folder as a jpg
    try:
        urllib.request.urlretrieve(img_url, img_file)
    except InputError as failure:
        raise InputError(
            description='Failed while retrieving image from URL!') from failure

    # Cropping part
    imageObject = Image.open(img_file)
    try:
        cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    except InputError as failure:
        raise InputError(
            description='Failed to crop, given crop size is invalid!') from failure

    cropped.save(img_file)
    # Set as new profile pic

    get_user_from_store(u_id)['profile_img_url'] = imageObject
    data_store.set(datastore)

    return {}
