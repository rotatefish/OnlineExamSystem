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


contest = Blueprint('contest', __name__)


@contest.route('/contest/create', methods=['GET', 'POST'])
@api_proto(api_pb2.CreateContestReq,
           api_pb2.CreateContestResp)
@inject(mysql=True, user_name=True)
def create_contest(req, mysql_client, user_name):
    mysql_client
