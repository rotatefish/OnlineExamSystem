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


QUESTION_PRIMARY_KEY = 'q_id'
EXAM_PAPER_PRIMARY_KEY = 'e_id'

MONGO_CONF = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'exam_online',
    'exam_paper_collection': 'exam_paper',
    'question_collection': 'question',
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
        self.exam_paper_collection = self.db[MONGO_CONF['exam_paper_collection']]
        self.question_collection = self.db[MONGO_CONF['question_collection']]

    ########## question ##########
    def get_question_count(self, filters):
        return helper.get_count(self.question_collection, filters)

    def create_question(self, question):
        err, total = self.get_question_count({})
        if not err.is_ok():
            return err, None
        question.q_id = total + 1
        return helper.insert_one(self.question_collection,
                                 db_pb2.Question,
                                 question,
                                 QUESTION_PRIMARY_KEY)

    def list_all_questions(self, filters=None, offset=None, limit=None):
        return helper.get_multiple(self.question_collection,
                                   cls=db_pb2.Question,
                                   filters=filters,
                                   offset=offset,
                                   limit=limit,
                                   primary_key=QUESTION_PRIMARY_KEY)

    def get_question_by_id(self, question_id):
        return helper.get_one(self.question_collection,
                              db_pb2.Question,
                              question_id,
                              QUESTION_PRIMARY_KEY)

    def update_question(self, question):
        return helper.update_one(self.question_collection,
                                 db_pb2.Question,
                                 question,
                                 QUESTION_PRIMARY_KEY)

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

        exam_paper.e_id = total + 1

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
