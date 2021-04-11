import sys
import os
import json

from http import HTTPStatus
from flask import Blueprint, session, request
from gen.proto import api_pb2, db_pb2
from api.decorators import api_proto, inject, get_user_name
from gen.proto.api_pb2 import ErrorResp, EmptyReq, EmptyResp


from google.protobuf import json_format, text_format

user = Blueprint('user', __name__)


@user.route('/user/login', methods=['POST'])
@api_proto(api_pb2.LoginReq,
           api_pb2.LoginResp)
@inject(mysql=True)
def user_login(req, mysql_client):
    err, user = mysql_client.get_user_by_id(req.uid)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="error")
    if user.password != req.password:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="wrong password")

    session['username'] = user.name
    session['uid'] = user.uid

    return HTTPStatus.OK, api_pb2.GetUserInfoResp(user=user)


@user.route('/user/register', methods=['POST'])
@api_proto(api_pb2.RegisterReq,
           api_pb2.RegisterResp)
@inject(mysql=True)
def user_register(req, mysql_client):

    role = db_pb2.User.Role.ADMIN
    err, user = mysql_client.create_user(req.uid,
                                         req.name,
                                         role,
                                         req.password)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="error")
    return HTTPStatus.OK, ErrorResp(err_msg="debug")


@user.route('/user/current', methods=['POST'])
@api_proto(api_pb2.EmptyReq,
           api_pb2.fetchCurrentUserResp)
@inject(mysql=True)
def fetch_current_user(req, mysql_client):

    username = get_user_name()
    return HTTPStatus.OK, api_pb2.fetchCurrentUserResp(name=username)



@user.route('/user/get', methods=['POST'])
@api_proto(api_pb2.GetUserInfoReq,
           api_pb2.GetUserInfoResp)
@inject(mysql=True)
def get_user_info(req, mysql_client):

    err, user = mysql_client.get_user_by_id(req.uid)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="error")
    return HTTPStatus.OK, api_pb2.GetUserInfoResp(user=user)
