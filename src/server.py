# from pickle import APPEND
# from socket import AF_PPPOX

import sys
import signal
from json import dumps
from urllib import response
from flask import Flask, request, abort
from flask_cors import CORS
from auth import auth_register_v2, auth_login_v2, auth_logout_v1
from error import AccessError, InputError
from other import is_valid_token, token_create
from user import user_profile_v1
from json import dumps
import config
import jwt
import pickle


APP = Flask(__name__)

# return dumps({}) if empty
# must return smth


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    arguments = request.get_json()
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


@APP.route("/clear/v1", methods=["DELETE"])
def clear_v1():
    '''
    Input Types:
    None

    Sets data in data.p to a default dictionary of empty lists
    '''
    DATA_STRUCTURE = {
        "users": [],
        "channels": [],
        "dms": [],
        "messages": [],
    }
    with open("data.p", "wb") as W_FILE:
        W_FILE.write(pickle.dumps(DATA_STRUCTURE))

    return dumps({})


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    arguments = request.get_json()
    print("LOGIN Arguments are:")
    print(arguments)
    resp = auth_login_v2(arguments['email'], arguments['password'])
    return dumps(resp)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():

    arguments = request.get_json()
    resp = auth_logout_v1(arguments['token'])
    return dumps(resp)


@APP.route("/user/profile/v1", methods=['GET'])
def user_profile_get():
    arguments = request.get_json()
    resp = user_profile_v1(arguments['token'], arguments['u_id'])
    return dumps(resp)


# NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port
