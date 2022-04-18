import re
from src.error import InputError, AccessError
from src.other import is_valid_token
from src.data_store import data_store
from src.config import url
from datetime import timezone
from flask import request
import requests
import datetime
import urllib.request
from PIL import Image
import PIL
import random
import string


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

    seam_stats = datastore['workspace_stats']
    # Used for calculating user involvement
    # General stats of seams
    num_channels_exist = len(datastore['channels'])
    num_dms_exist = len(datastore['dms'])
    num_messages_exist = seam_stats['messages_exist'][-1]['num_messages_exist']
    # User specific stats

    user_stats = datastore['users'][u_id - 1]['stats']
    num_channels_joined = user_stats['channels_joined'][-1]['num_channels_joined']
    num_dms_joined = user_stats['dms_joined'][-1]['num_dms_joined']
    num_msgs_sent = user_stats['messages_sent'][-1]['num_messages_sent']

    # Denominator
    denominator = sum([num_channels_exist, num_dms_exist, num_messages_exist])
    if denominator == 0:
        involvement = 0
    else:
        involvement = float(sum([num_channels_joined, num_dms_joined,
                                num_msgs_sent]))/float(denominator)
    if involvement > 1:
        involvement = 1

    user_stats['involvement_rate'] = involvement

    return {
        'user_stats': user_stats
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


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
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

    token_decoded = is_valid_token(token)
    if token_decoded == False:
        raise AccessError(description='False Token!')

    if x_end < x_start or y_end < y_start:
        raise InputError(description='Given crop dimensions are invalid!')

    datastore = data_store.get()
    u_id = token_decoded['u_id']

    # Determine if the online image exists, and is a .jpg file

    try:
        resp = urllib.request.urlopen(img_url)
    except ValueError as failure:
        raise InputError(
            description='Failed to connect to given img_url') from failure

    if resp.getcode() != 200:
        raise InputError(description='img_url http response is not 200!')

    # Construct path for where to save the cropped image
    random_string = ''.join(random.choice(string.ascii_letters)
                            for i in range(64))
    img_file = 'src/' + 'static/' + random_string + '.jpg'

    # Download image
    urllib.request.urlretrieve(img_url, img_file)

    # Cropping part
    try:
        imageObject = Image.open(img_file)
    except PIL.UnidentifiedImageError as failure:
        raise InputError(
            description='Not an image...') from failure

    # Check for format
    if imageObject.format != 'JPEG':
        raise InputError(description='Not a JPEG file!')

    x_width, y_height = imageObject.size
    # Check for cropping issues with size:
    if x_start > x_end or x_start < 0 or x_end > x_width:
        raise InputError(description='X crop values are wrong!')
    elif y_start > y_end or y_start < 0 or y_end > y_height:
        raise InputError(description='Y crop values are wrong!')

    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_file)

    # Set as new profile pic
    # Correct this...
    # Currently pastes in the file location into the url
    static_img_url = url + 'static/' + random_string + '.jpg'
    get_user_from_store(u_id)['profile_img_url'] = static_img_url
    data_store.set(datastore)

    return {}
