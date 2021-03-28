import sys
import os
import json

from flask import Blueprint, session, request
from gen.proto import api_pb2, db_pb2
from api.decorators import api_proto, inject


from google.protobuf import json_format, text_format

user = Blueprint('user', __name__)


@user.route('/current_user', methods=['GET', 'POST'])
@api_proto(db_pb2.User, db_pb2.User)
def current_user(req):

    print(req)
    return 200, api_pb2.ErrorResp(err_msg='debug')
    user = db_pb2.User()
    json_data = request.get_json(force=True)
    print(json_data)
    try:
        json_format.ParseDict(json_data, user)
    except Exception as e:
        print(e)
    print(user)
    return 200, json.dumps(json_data)
