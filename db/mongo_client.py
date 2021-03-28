import pymongo
import logging
import traceback
import time
import json
import datetime

from google.protobuf import json_format
from proto import db_pb2
from db import mongo_helper as helper

CONNECT_TIMEOUT_MS = 5000
SOCKET_TIMEOUT_MS = 60000
MAX_IDLE_TIME_MS = 1200000
MIN_POOL_SIZE = 10
MAX_POOL_SIZE = 50


CHOICE_QUESTION_PRIMARY_KEY = 'id'
JUDGE_QUESTION_PRIMARY_KEY = 'id'
EXAM_PAPER_PRIMARY_KEY = 'id'

MONGO_CONF = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'exam_online',
    'choice_question_collection': 'choice_question',
    'judge_question_collection': 'judge_question',
    'exam_paper_collection': 'exam_paper'
}


def pb_to_dict_converter(msg, primary_key=None):
    d = json_format.MessageToDict(msg, preserving_proto_field_name=True)
    if primary_key:
        d['_id'] = d[primary_key]
        del d[primary_key]
    return d


def dict_to_pb_converter(d, cls, primary_key=None):
    if '_id' in d:
        if primary_key:
            d[primary_key] = d['_id']
        del d['_id']
    obj = cls()
    json_format.ParseDict(d, obj)
    return obj


class MyMongoClient(object):

    def __init__(self):
        self.client = pymongo.MongoClient(
            host=MONGO_CONF['host'],
            port=MONGO_CONF['port'])

        self.db = self.client[MONGO_CONF['db_name']]
        self.choice_question_collection = self.db[MONGO_CONF['choice_question_collection']]
        self.judge_question_collection = self.db[MONGO_CONF['judge_question_collection']]
        self.exam_paper_collection = self.db[MONGO_CONF['exam_paper_collection']]

    ########## choice question ##########
    def get_choice_question_count(self, filters):

        return helper.get_count(self.choice_question_collection, filters)

    def get_choice_question_by_id(self, choice_question_id):
        return helper.get_one(self.choice_question_collection,
                              db_pb2.ChoiceQuestion,
                              choice_question_id,
                              CHOICE_QUESTION_PRIMARY_KEY)

    def update_choice_question(self, choice_question):
        return helper.update_one(self.choice_question_collection,
                                 db_pb2.ChoiceQuestion,
                                 choice_question,
                                 CHOICE_QUESTION_PRIMARY_KEY)

    def create_choice_question(self, choice_question):
        err, total = self.get_choice_question_count({})
        if not err.is_ok():
            return err, None

        choice_question.id = total + 1

        return helper.insert_one(self.choice_question_collection,
                                 db_pb2.ChoiceQuestion,
                                 choice_question,
                                 CHOICE_QUESTION_PRIMARY_KEY)

    def list_choice_questions(self, id_list=None, offset=None, limit=None):
        filter_list = []
        if id_list:
            filter_list = [{'_id': {'$in': id_list}}]

        filters = {'$and': filter_list} if len(filter_list) else None
        return helper.get_multiple(self.choice_question_collection,
                                   cls=db_pb2.ChoiceQuestion,
                                   filters=filters,
                                   offset=offset,
                                   limit=limit,
                                   primary_key=CHOICE_QUESTION_PRIMARY_KEY)

    ########## judge question ##########

    def get_judge_question_count(self, filters):
        return helper.get_count(self.judge_question_collection, filters)

    def get_judge_question_by_id(self, judge_question_id):
        return helper.get_one(self.judge_question_collection,
                              db_pb2.JudgeQuestion,
                              judge_question_id,
                              JUDGE_QUESTION_PRIMARY_KEY)

    def update_judge_question(self, judge_question):
        return helper.update_one(self.judge_question_collection,
                                 db_pb2.JudgeQuestion,
                                 judge_question,
                                 JUDGE_QUESTION_PRIMARY_KEY)

    def create_judge_question(self, judge_question):

        err, total = self.get_judge_question_count({})
        if not err.is_ok():
            return err, None

        judge_question.id = total + 1

        return helper.insert_one(self.judge_question_collection,
                                 db_pb2.JudgeQuestion,
                                 judge_question,
                                 JUDGE_QUESTION_PRIMARY_KEY)

    def list_judge_questions(self, id_list=None, offset=None, limit=None):
        filter_list = []
        if id_list:
            filter_list = [{'_id': {'$in': id_list}}]

        filters = {'$and': filter_list} if len(filter_list) else None
        return helper.get_multiple(self.judge_question_collection,
                                   cls=db_pb2.JudgeQuestion,
                                   filters=filters,
                                   offset=offset,
                                   limit=limit,
                                   primary_key=JUDGE_QUESTION_PRIMARY_KEY)

    ########## exam paper ##########
    def get_exam_paper_count(self, filters):
        return helper.get_count(self.exam_paper_collection, filters)

    def get_exam_paper_by_id(self, exam_paper_id):
        return helper.get_one(self.exam_paper_collection,
                              db_pb2.ExamPaper,
                              exam_paper_id,
                              EXAM_PAPER_PRIMARY_KEY)

    def update_exam_paper(self, exam_paper):
        return helper.insert_one(self.exam_paper_collection,
                                 db_pb2.ExamPaper,
                                 exam_paper,
                                 EXAM_PAPER_PRIMARY_KEY)

    def create_exam_paper(self, exam_paper):
        err, total = self.get_exam_paper_count({})
        if not err.is_ok():
            return err, None

        exam_paper.id = total + 1

        return helper.insert_one(self.exam_paper_collection,
                                 db_pb2.ExamPaper,
                                 exam_paper,
                                 EXAM_PAPER_PRIMARY_KEY)

    def list_exam_paper(self, id_list=None, offset=None, limit=None):
        filter_list = []
        if id_list:
            filter_list = [{'_id': {'$in': id_list}}]

        filters = {'$and': filter_list} if len(filter_list) else None
        return helper.get_multiple(self.exam_paper_collection,
                                   cls=db_pb2.ExamPaper,
                                   filters=filters,
                                   offset=offset,
                                   limit=limit,
                                   primary_key=EXAM_PAPER_PRIMARY_KEY)
