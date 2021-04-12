import json
import os
import re
import time

from http import HTTPStatus
from flask import Blueprint, session, request
from google.protobuf import json_format
from pprint import pprint

from proto.api_pb2 import EmptyReq, EmptyResp, ErrorResp
from proto import db_pb2
from proto import api_pb2
from api.decorators import api_proto, inject, login_required


question = Blueprint('question', __name__)


@question.route('/question/all_question/create', methods=['GET', 'POST'])
@api_proto(api_pb2.CreateAllQuestionReq,
           api_pb2.CreateAllQuestionResp)
@inject(mongo=True)
def create_question(req, mongo_client):

    q = db_pb2.Question()
    q.type = req.type
    q.description = req.description
    q.judge_data.CopyFrom(req.judge_data)
    q.choice_data.CopyFrom(req.choice_data)

    current_time = int(time.time())
    q.status = db_pb2.Status.ENABLED
    q.created_by = "admin"
    q.creation_time = current_time
    q.modified_time = current_time

    err, q = mongo_client.create_question(q)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="Failed to create normal question")

    return HTTPStatus.OK, ErrorResp(err_msg="Debug")


@question.route('/question/all_question/list', methods=['GET', 'POST'])
@api_proto(api_pb2.ListAllQuestionReq,
           api_pb2.ListAllQuestionResp)
@inject(mongo=True)
def list_all_question(req, mongo_client):
    limit = 10 if req.page_size < 1 or req.page_size > 100 else req.page_size
    offset = ((1 if req.current < 1 else req.current) - 1) * limit

    filter_list = []
    if req.filters:
        req_filters = req.filters
        if req_filters.q_id:
            filter_list.append({'_id': req_filters.q_id})
        if req_filters.description:
            pattern = re.compile('.*{}.*'.format(req_filters.description))
            filter_list.append({'description': pattern})
        if req_filters.type and req_filters.type != db_pb2.Question.Type.UNKNOWN:
            q_type = db_pb2.Question.Type.Name(req_filters.type)
            filter_list.append({'type': q_type})

    filters = {'$and': filter_list} if len(filter_list) else None

    err, total, questions = mongo_client.list_all_questions(
        filters=filters,
        offset=offset,
        limit=limit)

    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="Failed to get judge question list")

    return HTTPStatus.OK, api_pb2.ListAllQuestionResp(
        total=total,
        data=questions)
