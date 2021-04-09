import json
import os
import time

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

    for q_id in req.q_id_list:
        exam_paper.q_id_list.append(q_id)

    current_time = int(time.time())
    exam_paper.status = db_pb2.Status.ENABLED
    exam_paper.created_by = "admin"
    exam_paper.creation_time = current_time
    exam_paper.modified_time = current_time

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

    filters = {'_id': {'$in': list(exam_paper.q_id_list)}}
    err, total, questions = mongo_client.list_all_questions(filters)
    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="failed to get exam paper, No choice questions")

    return HTTPStatus.OK, api_pb2.GetExamPaperResp(
        exam_paper=exam_paper,
        questions=questions)


@exam.route('/exam/exam_paper/list', methods=['GET', 'POST'])
@api_proto(api_pb2.ListExamPaperReq,
           api_pb2.ListExamPaperResp)
@inject(mongo=True)
def list_exam_paper(req, mongo_client):
    limit = 10 if req.page_size < 1 or req.page_size > 100 else req.page_size
    offset = ((1 if req.current < 1 else req.current) - 1) * limit

    filter_list = []
    if req.filters:
        req_filters = req.filters
        if req_filters.e_id:
            filter_list.append({'_id': req_filters.e_id})
        if req_filters.title:
            pattern = re.compile('.*{}.*'.format(req_filters.title))
            filter_list.append({'description': pattern})

    filters = {'$and': filter_list} if len(filter_list) else None

    err, total, exam_papers = mongo_client.list_exam_papers(
        filters=filters,
        offset=offset,
        limit=limit)

    if not err.is_ok():
        return HTTPStatus.BAD_REQUEST, ErrorResp(err_msg="Failed to get judge question list")

    return HTTPStatus.OK, api_pb2.ListExamPaperResp(
        total=total,
        data=exam_papers)
