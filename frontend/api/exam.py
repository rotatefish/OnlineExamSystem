import json
import os

from http import HTTPStatus
from flask import Blueprint, session, request
from pprint import pprint

from proto.api_pb2 import EmptyReq, EmptyResp, ErrorResp
from proto import db_pb2
from proto import api_pb2

from api.decorators import api_proto, inject

exam = Blueprint('exam', __name__)


@exam.route('/exam/exam_paper/create', methods=['POST'])
@api_proto(api_pb2.CreateExamPaperReq,
           api_pb2.CreateExamPaperResp)
@inject(mongo=True)
def create_exam_paper(req, mongo_client):
    exam_paper = db_pb2.ExamPaper()
    exam_paper.title = req.title
    #exam_paper.judge_id_list = req.judge_id_list
    #exam_paper.choice_id_list = req.choice_id_list
    for q_id in req.judge_id_list:
        exam_paper.judge_id_list.append(q_id)

    for q_id in req.choice_id_list:
        exam_paper.choice_id_list.append(q_id)

    err, exam_paper = mongo_client.create_exam_paper(exam_paper)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, api_pb2.ErrorResp(err_msg=str(err))

    return HTTPStatus.OK, api_pb2.CreateExamPaperResp(exam_paper=exam_paper)


@exam.route('/exam/exam_paper/get', methods=['POST', 'GET'])
@api_proto(api_pb2.GetExamPaperReq,
           api_pb2.GetExamPaperResp)
@inject(mongo=True)
def get_exam_paper(req, mongo_client):
    err, exam_paper = mongo_client.get_exam_paper_by_id(req.e_id)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="failed to get exam paper, err is {}".format(err))

    filters = {'_id': {'$in': list(exam_paper.choice_id_list)}}
    err, total, choice_questions = mongo_client.list_choice_questions(filters)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="failed to get exam paper, No choice questions")

    filters = {'_id': {'$in': list(exam_paper.judge_id_list)}}
    err, total, judge_questions = mongo_client.list_judge_questions(filters)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="failed to get exam paper,  No judge questions")

    return HTTPStatus.OK, api_pb2.GetExamPaperResp(
        exam_paper=exam_paper,
        judge_questions=judge_questions,
        choice_questions=choice_questions)


@exam.route('/exam/exam_paper/list', methods=['GET', 'POST'])
@api_proto(api_pb2.ListExamPaperReq,
           api_pb2.ListExamPaperResp)
@inject(mongo=True)
def list_exam_paper(req, mongo_client):
    id_list = list(req.exam_id_list)
    err, total, exams = mongo_client.list_exam_paper(id_list)

    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="debug")

    results = {}
    for exam in exams:
        exam_id = exam.id
        results[exam_id] = json_format.MessageToDict(exam)
    resp_dict = {
        "exam_papers": results
    }
    resp = api_pb2.ListExamPaperResp()
    json_format.ParseDict(resp_dict, resp)
    return HTTPStatus.OK, resp
