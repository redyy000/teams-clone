# from pickle import APPEND
# from socket import AF_PPPOX

from src.config import port
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1
import sys
import signal
from json import dumps
from urllib import response
from flask import Flask, request, abort
from flask_cors import CORS
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.other import clear_v1, is_valid_token
from src.channels import channels_create_v2, channels_listall_v2
from src.channel import channel_leave_v1, channel_addowner_v1, channel_invite_v2, channel_details_v2


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


APP = Flask(__name__)
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


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    arguments = request.get_json()
    resp = auth_login_v2(arguments['email'], arguments['password'])
    return dumps(resp)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    arguments = request.get_json()
    resp = auth_logout_v1(arguments['token'])
    return dumps(resp)
    
@APP.route("/channels/create/v2", methods = ["POST"])
def channels_create():
    arguments = request.get_json()
    resp = channels_create_v2(arguments["token"], arguments["name"], arguments["is_public"])
    return dumps(resp)

@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    clear_v1()
    return dumps({})

@APP.route("/user/profile/v1", methods=['GET'])
def user_profile_get():
    arguments = request.get_json()
    resp = user_profile_v1(arguments['token'], arguments['u_id'])
    return dumps(resp)

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    payload = request.get_json()
    token = payload['token']
    channel_invite_v2(token, payload['channel_id'], payload['user_id'])
    return dumps({})    

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    arguments = request.get_json()
    resp = user_profile_setemail_v1(arguments['token'], arguments['email'])
    return dumps(resp)

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    arguments = request.get_json()
    resp = user_profile_sethandle_v1(
        arguments['token'], arguments['handle_str'])
    return dumps(resp)


@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    arguments = request.get_json()
    resp = user_profile_setname_v1(
        arguments['token'], arguments['name_first'], arguments['name_last'])
    return dumps(resp)

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    returnvalue = channels_listall_v2(token)
    return dumps(returnvalue)

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    payload = request.get_json()
    token = payload['token']
    channel_leave_v1(token, payload['channel_id'])
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['user_id']
    channel_addowner_v1(token, channel_id, u_id)
    return dumps({})

# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=port)  # Do not edit this port

