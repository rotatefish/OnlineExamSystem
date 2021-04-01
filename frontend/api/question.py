import json
import os
import re

from flask import Blueprint, session, request
from google.protobuf import json_format
from pprint import pprint

from proto.api_pb2 import EmptyReq, EmptyResp, ErrorResp
from proto import db_pb2
from proto import api_pb2
from api.decorators import api_proto, inject


question = Blueprint('question', __name__)


@question.route('/question/choice_question/create', methods=['POST'])
@api_proto(api_pb2.CreateChoiceQuestionReq,
           api_pb2.CreateChoiceQuestionResp)
@inject(mongo=True)
def create_choice_question(req, mongo_client):
    q = db_pb2.ChoiceQuestion()
    q.type = req.type
    q.description = req.description
    q.single_answser = req.single_answser
    for answser in req.multiple_answser:
        q.multiple_answser.append(answser)
    for content in req.contents:
        q.contents.append(content)

    err, q = mongo_client.create_choice_question(q)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.CreateChoiceQuestionResp(choice_question=q)


@question.route('/question/choice_question/get', methods=['GET', 'POST'])
@api_proto(api_pb2.GetChoiceQuestionReq,
           api_pb2.GetChoiceQuestionResp)
@inject(mongo=True)
def get_choice_question(req, mongo_client):
    err, question = mongo_client.get_choice_question_by_id(req.q_id)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.GetChoiceQuestionResp(choice_question=question)


@question.route('/question/choice_question/list', methods=['GET', 'POST'])
@api_proto(api_pb2.ListChoiceQuestionReq,
           api_pb2.ListChoiceQuestionResp)
@inject(mongo=True)
def list_choice_questions(req, mongo_client):
    limit = 10 if req.page_size < 1 or req.page_size > 100 else req.page_size
    offset = ((1 if req.current < 1 else req.current) - 1) * limit

    filter_list = []
    if req.filters:
        req_filters = req.filters
        if req_filters.id:
            filter_list.append({'_id': req_filters.q_id})
        if req_filters.description:
            pattern = re.compile('.*{}.*'.format(req_filters.description))
            filter_list.append({'description': pattern})
    filters = {'$and': filter_list} if len(filter_list) else None

    err, total, questions = mongo_client.list_choice_questions(
        filters=filters,
        offset=offset,
        limit=limit)

    if not err.is_ok():
        return 500, ErrorResp(err_msg="Failed to get choice question list")

    return 200, api_pb2.ListChoiceQuestionResp(
        total=total,
        data=questions)


@question.route('/question/judge_question/create', methods=['POST'])
@api_proto(api_pb2.CreateJudgeQuestionReq,
           api_pb2.CreateJudgeQuestionResp)
@inject(mongo=True)
def create_judge_question(req, mongo_client):
    question = db_pb2.JudgeQuestion()
    question.description = req.description
    question.answser = req.answser

    err, question = mongo_client.create_judge_question(question)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.CreateJudgeQuestionResp(judge_question=question)


@question.route('/question/judge_question/get', methods=['GET', 'POST'])
@api_proto(api_pb2.GetJudgeQuestionReq,
           api_pb2.GetJudgeQuestionResp)
@inject(mongo=True)
def get_judge_question(req, mongo_client):
    err, question = mongo_client.get_judge_question_by_id(req.q_id)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.GetJudgeQuestionResp(judge_question=question)


@question.route('/question/judge_question/list', methods=['GET', 'POST'])
@api_proto(api_pb2.ListJudgeQuestionReq,
            api_pb2.ListJudgeQuestionResp)
@inject(mongo=True)
def list_judge_question(req, mongo_client):
    limit = 10 if req.page_size < 1 or req.page_size > 100 else req.page_size
    offset = ((1 if req.current < 1 else req.current) - 1) * limit

    filter_list = []
    if req.filters:
        req_filters = req.filters
        if req_filters.id:
            filter_list.append({'_id': req_filters.q_id})
        if req_filters.description:
            pattern = re.compile('.*{}.*'.format(req_filters.description))
            filter_list.append({'description': pattern})
    filters = {'$and': filter_list} if len(filter_list) else None

    err, total, questions = mongo_client.list_judge_questions(
        filters=filters,
        offset=offset,
        limit=limit)

    if not err.is_ok():
        return 500, ErrorResp(err_msg="Failed to get judge question list")

    return 200, api_pb2.ListJudgeQuestionResp(
        total=total,
        data=questions)