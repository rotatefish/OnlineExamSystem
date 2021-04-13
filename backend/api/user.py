import sys
import os
import json
import time

from http import HTTPStatus
from flask import Blueprint, session, request
from gen.proto import api_pb2, db_pb2
from api.decorators import api_proto, inject, get_user_name, login_required
from gen.proto.api_pb2 import ErrorResp, EmptyReq, EmptyResp
from api.auth import Auth

from google.protobuf import json_format, text_format

user = Blueprint('user', __name__)


@user.route('/user/register', methods=['POST'])
@api_proto(api_pb2.RegisterReq,
           api_pb2.RegisterResp)
@inject(mysql=True)
def user_register(req, mysql_client):

    role = db_pb2.User.Role.ADMIN
    gender = db_pb2.User.Gender.MALE
    avatar = 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png'

    err, user = mysql_client.create_user(user_id=req.user_id,
                                         name=req.name,
                                         role=role,
                                         email=req.email,
                                         avatar=avatar,
                                         gender=gender,
                                         password=req.password)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="注册失败")
    return HTTPStatus.OK, api_pb2.RegisterResp(user=user)


@user.route('/user/login', methods=['POST'])
@api_proto(api_pb2.LoginReq,
           api_pb2.LoginResp)
@inject(mysql=True)
def user_login(req, mysql_client):
    err, user = mysql_client.get_user_by_id(req.user_id)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="用户未注册")

    if user.password != req.password:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="密码错误")

    login_time = int(time.time())
    token = Auth.encode_auth_token(req.user_id, login_time)
    session['user_name'] = user.name
    session['user_id'] = user.user_id
    return HTTPStatus.OK, api_pb2.LoginResp(token=token)


@user.route('/user/logout', methods=['POST'])
@api_proto(api_pb2.LogoutReq,
           api_pb2.LogoutResp)
@inject(mysql=True, user_id=True)
def user_logout(req, mysql_client, user_id):
    if not user_id:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="用户未登录")
    err, user = mysql_client.get_user_by_id(user_id)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="用户未注册")

    session.clear()
    return HTTPStatus.OK, api_pb2.LogoutResp()


@user.route('/user/current', methods=['GET', 'POST'])
@api_proto(api_pb2.EmptyReq,
           api_pb2.CurrentUserResp)
@inject(mysql=True, user_name=True, user_id=True)
def fetch_current_user(req, mysql_client, user_name, user_id):

    if not user_id:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg='用户未登录')
    err, user = mysql_client.get_user_by_id(user_id)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg='用户未登录')

    return HTTPStatus.OK, api_pb2.CurrentUserResp(name=user_name,
                                                  user_id=user_id,
                                                  avatar=user.avatar,
                                                  email=user.email,
                                                  role=user.role,
                                                  gender=user.gender)


@user.route('/user/get', methods=['POST'])
@api_proto(api_pb2.GetUserInfoReq,
           api_pb2.GetUserInfoResp)
@inject(mysql=True)
def get_user_info(req, mysql_client):

    err, user = mysql_client.get_user_by_id(req.user_id)
    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="找不到该用户")
    return HTTPStatus.OK, api_pb2.GetUserInfoResp(user=user)


@user.route('/user/list', methods=['GET', 'POST'])
@api_proto(api_pb2.QueryAllUserReq,
           api_pb2.QueryAllUserResp)
@inject(mysql=True)
def query_all_user(req, mysql_client):

    limit = 10 if req.page_size < 1 or req.page_size > 100 else req.page_size
    offset = ((1 if req.current < 1 else req.current) - 1) * limit

    err, total, users = mysql_client.query_all_user(offset=offset,
                                                    limit=limit,
                                                    user_id=req.filters.user_id,
                                                    name=req.filters.name,
                                                    role=req.filters.role,
                                                    gender=req.filters.gender)

    if err:
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="找不到该用户")
    return HTTPStatus.OK, api_pb2.QueryAllUserResp(total=total,
                                                   data=users)
