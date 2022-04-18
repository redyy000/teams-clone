# from pickle import APPEND
# from socket import AF_PPPOX

from src.config import port
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, user_profile_uploadphoto_v1, user_stats_v1
from src.users import users_list_all_v1, users_stats_v1
import sys
import signal
from json import dumps
from urllib import response
from flask import Flask, request, abort, send_from_directory, jsonify
from flask_cors import CORS
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.other import clear_v1, search_v1, notifications_get_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_invite_v2, channel_join_v2, channel_messages_v2, channel_leave_v1, channel_addowner_v1, channel_removeowner_v1
from src.dm import dm_create_v1, dm_details_v1, dm_list_v1, dm_remove_v1, dm_leave_v1, dm_messages_v1
from src.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1, message_share_v1
from src.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.message_send_later import message_sendlater_dm_v1, message_sendlater_v1
from src.data_store import data_store
from src.standup import standup_start_v1, standup_send_v1, standup_active_v1, standup_thread

APP = Flask(__name__)


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
    resp = auth_register_v2(arguments['email'],
                            arguments['password'],
                            arguments['name_first'],
                            arguments['name_last'])
    data_store.save()
    return dumps(resp)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    arguments = request.get_json()
    resp = auth_login_v2(arguments['email'], arguments['password'])
    data_store.save()
    return dumps(resp)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    arguments = request.get_json()
    resp = auth_logout_v1(arguments['token'])
    data_store.save()
    return dumps(resp)


@APP.route("/channels/create/v2", methods=["POST"])
def channels_create():
    arguments = request.get_json()
    resp = channels_create_v2(
        arguments["token"], arguments["name"], arguments["is_public"])
    data_store.save()
    return dumps(resp)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token', )
    channel_id = request.args.get('channel_id', type=int)
    start = request.args.get('start', type=int)
    returnvalue = channel_messages_v2(token, channel_id, start)
    data_store.save()
    return dumps(returnvalue)


@APP.route("/channel/details/v2", methods=["GET"])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id', type=int)
    returnvalue = channel_details_v2(token, channel_id)
    data_store.save()
    return dumps(returnvalue)


@APP.route("/channels/list/v2", methods=["GET"])
def channels_list():
    token = request.args.get('token')
    resp = channels_list_v2(token)
    data_store.save()
    return dumps(resp)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    returnvalue = channels_listall_v2(token)
    data_store.save()
    return dumps(returnvalue)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    payload = request.get_json()
    token = payload['token']
    channel_join_v2(token, payload['channel_id'])
    data_store.save()
    return dumps({})


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    payload = request.get_json()
    token = payload['token']
    channel_invite_v2(token, payload['channel_id'], payload['u_id'])
    data_store.save()
    return dumps({})


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    payload = request.get_json()
    token = payload['token']
    channel_leave_v1(token, payload['channel_id'])
    data_store.save()
    return dumps({})


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    channel_addowner_v1(token, channel_id, u_id)
    data_store.save()
    return dumps({})


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    channel_removeowner_v1(token, channel_id, u_id)
    data_store.save()
    return dumps({})


@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    clear_v1()
    data_store.save()
    return dumps({})


@APP.route("/user/profile/v1", methods=['GET'])
def user_profile_get():
    token = request.args.get('token', type=str)
    u_id = request.args.get('u_id', type=int)
    resp = user_profile_v1(token, u_id)
    data_store.save()
    return dumps(resp)


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail():
    arguments = request.get_json()
    resp = user_profile_setemail_v1(arguments['token'], arguments['email'])
    data_store.save()
    return dumps(resp)


@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    arguments = request.get_json()
    resp = user_profile_sethandle_v1(
        arguments['token'], arguments['handle_str'])
    data_store.save()
    return dumps(resp)


@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname():
    arguments = request.get_json()
    resp = user_profile_setname_v1(
        arguments['token'], arguments['name_first'], arguments['name_last'])
    data_store.save()
    return dumps(resp)


@APP.route("/users/all/v1", methods=['GET'])
def users_list_all():
    token = request.args.get('token', type=str)
    resp = users_list_all_v1(
        token)
    data_store.save()
    return dumps(resp)


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    arguments = request.get_json()
    resp = dm_create_v1(
        arguments['token'], arguments['u_ids'])
    data_store.save()
    return dumps(resp)


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token', type=str)
    resp = dm_list_v1(
        token)
    data_store.save()
    return dumps(resp)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    arguments = request.get_json()
    resp = dm_remove_v1(
        arguments['token'], arguments['dm_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = request.args.get('token', type=str)
    dm_id = request.args.get('dm_id', type=int)
    resp = dm_details_v1(
        token, dm_id)
    data_store.save()
    return dumps(resp)


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    arguments = request.get_json()
    resp = dm_leave_v1(
        arguments['token'], arguments['dm_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    arguments = request.get_json()
    resp = message_senddm_v1(
        arguments['token'], arguments['dm_id'], arguments['message'])
    data_store.save()
    return dumps(resp)


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token', type=str)
    dm_id = request.args.get('dm_id', type=int)
    start = request.args.get('start', type=int)

    resp = dm_messages_v1(
        token, dm_id, start)
    data_store.save()
    return dumps(resp)


@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    arguments = request.get_json()
    resp = message_send_v1(
        arguments['token'], arguments['channel_id'], arguments['message'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    arguments = request.get_json()
    resp = message_edit_v1(
        arguments['token'], arguments['message_id'], arguments['message'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    arguments = request.get_json()
    resp = message_remove_v1(
        arguments['token'], arguments['message_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    arguments = request.get_json()
    resp = message_react_v1(
        arguments['token'], arguments['message_id'], arguments['react_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    arguments = request.get_json()
    resp = message_unreact_v1(
        arguments['token'], arguments['message_id'], arguments['react_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    arguments = request.get_json()
    resp = message_pin_v1(
        arguments['token'], arguments['message_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    arguments = request.get_json()
    resp = message_unpin_v1(
        arguments['token'], arguments['message_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_permission_change():
    arguments = request.get_json()
    resp = admin_userpermission_change_v1(
        arguments['token'], arguments['u_id'], arguments['permission_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    arguments = request.get_json()
    resp = admin_user_remove_v1(
        arguments['token'], arguments['u_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    length = payload['length']
    resp = standup_start_v1(token, channel_id, length)
    data_store.save()
    return dumps(resp)


@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    resp = standup_send_v1(token, channel_id, message)
    data_store.save()
    return dumps(resp)


@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    token = request.args.get('token', type=str)
    channel_id = request.args.get('channel_id', type=int)
    resp = standup_active_v1(token, channel_id)
    data_store.save()
    return dumps(resp)


@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_passwordreset_request():
    arguments = request.get_json()
    resp = auth_passwordreset_request_v1(arguments['email'])
    data_store.save()
    return dumps(resp)


@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_passwordreset_reset():
    arguments = request.get_json()
    resp = auth_passwordreset_reset_v1(
        arguments['reset_code'], arguments['new_password'])
    data_store.save()
    return dumps(resp)


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
    arguments = request.get_json()
    resp = user_profile_uploadphoto_v1(
        arguments['token'], arguments['img_url'], arguments['x_start'], arguments['y_start'], arguments['x_end'], arguments['y_end'])
    data_store.save()
    return dumps(resp)


@APP.route("/static/<path:path>")
def return_photo_static(path):
    return send_from_directory('', path)


@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')

    resp = user_stats_v1(token)
    data_store.save()
    return dumps(resp)


@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')

    resp = users_stats_v1(token)
    data_store.save()
    return dumps(resp)


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    arguments = request.get_json()
    resp = message_sendlater_v1(
        arguments['token'], arguments['channel_id'], arguments['message'], arguments['time_sent'])
    data_store.save()
    return dumps(resp)


@APP.route("/search/v1", methods=['GET'])
def search():
    token = request.args.get('token', type=str)
    query_str = request.args.get('query_str', type=str)
    resp = search_v1(
        token, query_str)

    data_store.save()
    return dumps(resp)


@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlater_dm():
    arguments = request.get_json()
    resp = message_sendlater_dm_v1(
        arguments['token'], arguments['dm_id'], arguments['message'], arguments['time_sent'])
    data_store.save()
    return dumps(resp)


@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    arguments = request.get_json()
    resp = message_share_v1(arguments['token'], arguments['og_message_id'],
                            arguments['message'], arguments['channel_id'], arguments['dm_id'])
    data_store.save()
    return dumps(resp)


@APP.route("/notifications/get/v1", methods=['GET'])
def notifications():
    token = request.args.get('token')
    notifications = notifications_get_v1(token)
    return jsonify(notifications)


# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=port)  # Do not edit this port
