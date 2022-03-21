# from pickle import APPEND
# from socket import AF_PPPOX
from urllib import response
from flask import Flask, request, abort
from auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.error import AccessError
from src.other import is_valid_token
from user import user_profile_v1
from other import token_create, token_decode, is_valid_token
from json import dumps
import jwt


APP = Flask(__name__)

# return dumps({}) if empty
# must return smth


@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():

    arguments = request.get_json

    # user_data is of form:
    '''
    user = {
        'u_id'  : auth_user_id,
        'email' : email,
        'password'   : hash(password),
        'name_first' : name_first,
        'name_last'  : name_last,
        'handle_str' : create_handle_str(store, name_first, name_last),
        'session_id_list' : [1]
    }
    '''
    # What happens when auth_register_v2 throws an exception?
    resp = auth_register_v2(arguments['email'],
                            arguments['password'],
                            arguments['name_first'],
                            arguments['name_last'])
    return dumps(resp)


@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    arguments = request.get_json
    resp = auth_login_v2(arguments['email'], arguments['password'])
    return dumps(resp)


@APP.route('/auth/logout/v1', methods=['POST'])
def auth_logout():

    arguments = request.get_json()

    resp = auth_logout_v1(arguments['token'])
    return dumps(resp)


@APP.route('/user/profile/v1', methods=['GET'])
def user_profile_get():
    arguments = request.get_json()
    resp = user_profile_v1(arguments['token'], arguments['u_id'])
    return dumps(resp)
