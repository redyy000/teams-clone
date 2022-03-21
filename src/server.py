from flask import Flask, request, abort
from auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.error import AccessError
from src.other import is_valid_token
from other import token_create, token_decode, is_valid_token
from json import dumps
import jwt
from src.other import is_valid_token
from src.channel import channel_invite_v1, channel_join_v1, channel_messages_v1

APP = Flask(__name__)
SECRET = 'PLACEHOLDER'


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
    payload = request.get_json()
    token = payload['token']
    user_info = is_valid_token(token, SECRET)

    if user_info is False:
        raise AccessError("Invalid Token")

    user_id = user_info['user_id']
    channel_join_v1(user_id, payload['channel_id'])
    return dumps({})


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
    payload = request.get_json()
    token = payload['token']
    user_info = is_valid_token(token, SECRET)

    if user_info is False:
        raise AccessError("Invalid Token")

    user_id = user_info['user_id']
    channel_invite_v1(user_id, payload['channel_id'])
    return dumps({})


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    user_info = is_valid_token(token, SECRET)

    if user_info is False:
        raise AccessError("Invalid Token")

    user_id = user_info['user_id']
    returnvalue = channel_messages_v1(user_id, channel_id, start)

    return dumps(returnvalue)
