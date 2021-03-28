import json
import os

from flask import Blueprint, session, request
from google.protobuf import json_format
from pprint import pprint

from proto.api_pb2 import EmptyReq, EmptyResp, ErrorResp
from proto import db_pb2
from proto import api_pb2
from api.decorators import api_proto, inject


question = Blueprint('question', __name__)


@question.route('/question/choice_question/create', methods=['GET', 'POST'])
@api_proto(api_pb2.CreateChoiceQuestionReq,
           api_pb2.CreateChoiceQuestionResp)
@inject(mongo=True)
def create_choice_question(req, mongo_client):
    question = db_pb2.ChoiceQuestion()
    question.description = req.description
    question.answser = req.answser
    question.option_a = req.option_a
    question.option_b = req.option_b
    question.option_c = req.option_c
    question.option_d = req.option_d

    err, question = mongo_client.create_choice_question(question)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.CreateChoiceQuestionResp(choice_question=question)


@question.route('/question/choice_question/get', methods=['GET', 'POST'])
@api_proto(api_pb2.GetChoiceQuestionReq,
           api_pb2.GetChoiceQuestionResp)
@inject(mongo=True)
def get_choice_question(req, mongo_client):
    err, question = mongo_client.get_choice_question_by_id(req.id)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.GetChoiceQuestionResp(choice_question=question)


@question.route('/question/choice_question/list', methods=['GET', "POST"])
@api_proto(api_pb2.ListChoiceQuestionReq,
           api_pb2.ListChoiceQuestionResp)
@inject(mongo=True)
def list_choice_questions(req, mongo_client):
    id_list = list(req.question_id_list)
    err, total, questions = mongo_client.list_choice_questions(id_list)

    if not err.is_ok():
        return 500, ErrorResp(err_msg="debug")

    results = {}
    for q in questions:
        q_id = q.id
        results[q_id] = json_format.MessageToDict(q)
    resp_dict = {
        "choice_questions": results
    }
    resp = api_pb2.ListChoiceQuestionResp()
    json_format.ParseDict(resp_dict, resp)
    return 200, resp


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


@question.route('/question/judge_question/get', methods=['POST'])
@api_proto(api_pb2.GetJudgeQuestionReq,
           api_pb2.GetJudgeQuestionResp)
@inject(mongo=True)
def get_judge_question(req, mongo_client):
    err, question = mongo_client.get_judge_question_by_id(req.id)
    if not err.is_ok():
        return 500, api_pb2.ErrorResp(err_msg=str(err))

    return 200, api_pb2.GetJudgeQuestionResp(judge_question=question)
