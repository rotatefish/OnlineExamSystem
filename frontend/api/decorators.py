import functools
import flask
import json
import traceback

from flask import jsonify, request, session
from proto.api_pb2 import EmptyReq, EmptyResp, ErrorResp
from google.protobuf import json_format
from api.dal import get_mongo_client_dal
from db.mysql_client import create_or_get_mysql_client


def inject(mysql=False, mongo=False, user_name=False):
    def inject_inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if mysql:
                kwargs['mysql_client'] = create_or_get_mysql_client()
            if mongo:
                kwargs['mongo_client'] = get_mongo_client_dal()
            if user_name:
                kwargs['user_name'] = 'user_name'

            return f(*args, **kwargs)
        return wrapper
    return inject_inner


def to_json_resp(http_code, msg, is_pb2=False):
    return flask.Response(
        response=json_format.MessageToJson(
            msg,
            including_default_value_fields=not is_pb2,
            sort_keys=True
        ),
        status=http_code,
        mimetype='application/json'
    )


def to_err_resp(http_code, err_msg):
    error_resp = ErrorResp(err_msg=err_msg)
    return to_json_resp(http_code, error_resp)


def api_proto(req_proto, resp_proto):
    def api_proto_inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not request.data.strip():
                json_data = {}
            else:
                json_data = request.get_json(force=True)
                if not isinstance(json_data, dict):
                    return to_err_resp(500, 'JSON format error')

            for _, key in enumerate(request.form):
                json_data[key] = request.form[key]

            for k, v in kwargs.items():
                json_data[k] = v

            for k, v in request.args.items():
                json_data[k] = v

            json_str = json.dumps(json_data)
            req_msg = req_proto()

            try:
                json_format.Parse(json_str, req_msg)
            except json_format.ParseError as e:
                return to_err_resp(500, str(e))

            try:
                code, resp_msg = f(req=req_msg)
            except Exception as e:
                traceback.print_exc()
                return to_err_resp(500, str(e))

            is_pb2 = False

            return to_json_resp(code, resp_msg, is_pb2)
        return wrapper
    return api_proto_inner


def get_user_name():
    user_name = session.get('username', None)
    if user_name:
        return user_name

    return 'admin'