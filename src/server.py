# from pickle import APPEND
# from socket import AF_PPPOX
from urllib import response
from flask import Flask, request, abort
from auth import auth_register_v2, auth_login_v2, auth_logout_v1
from other import token_create, token_decode
from json import dumps
import jwt


APP = Flask(__name__)

# return dumps({}) if empty 
# must return smth


@APP.route('/auth/register/v2', methods = ['POST'])

def user_register():
    
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


@APP.route('/auth/login/v2', methods = ['POST'])
def user_login():
    arguments = request.get_json
    resp = auth_login_v2(arguments['email'], arguments['password'])
    return dumps(resp)

    
@APP.route('/auth/logout/v1', methods = ['POST'])
def user_logout():
    token = request.get_json()
    token_decoded = token_decode(token)
    resp = auth_logout_v1(token_decoded)
    return dumps(resp)
    

    
