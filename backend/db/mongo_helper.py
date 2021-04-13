import traceback
import functools
import logging
import json
from proto import db_pb2
from google.protobuf import json_format


class Error(object):
    """
    Error code enum for mongo client
    """
    OK = 0
    UNKNOWM = 1
    NOT_FOUND = 2
    MULTIPLE_RESULT = 3
    INVALID = 4
    CONFILICT = 5

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def is_ok(self):
        return self.code == self.OK

    def is_not_found(self):
        return self.code == self.NOT_FOUND

    @staticmethod
    def ok():
        return Error(Error.OK, 'OK')

    def __repr__(self):
        if self.code == Error.OK:
            return 'OK'
        else:
            return 'ERROR: ' + self.msg


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


#####
def get_count(collection, filters):
    try:
        return Error.ok(), collection.find(filters).count()
    except Exception as ex:
        logging.error("get count failed, err is {}".format(ex))
        traceback.print_exc()
        return Error(Error.UNKNOWM, str(ex)), 0


def get_one(collection, cls, id, primary_key=None):
    try:
        result = collection.find_one({'_id': id})
        if result is None:
            return Error(Error.NOT_FOUND, 'failed to find {} object by {}'.format(cls, id)), None
        return Error.ok(), dict_to_pb_converter(result, cls, primary_key)
    except Exception as ex:
        logging.error(
            'get {} object by {} failed, exception is {}'.format(cls, id, ex))
        traceback.print_exc()
        return Error(Error.UNKNOWM, ex), None


def get_multiple(collection, cls, filters=None, offset=None, limit=None, sort=None, primary_key=None):
    try:
        cursor = collection.find(filters)
        if offset:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        if sort:
            cursor = cursor.sort(sort)
        results = [dict_to_pb_converter(r, cls, primary_key) for r in cursor]
        return Error.ok(), cursor.count(), results
    except Exception as ex:
        logging.error(
            'get {} object by {} failed, exception is {}'.format(cls, filters, ex))
        traceback.print_exc()
        return Error(Error.UNKNOWM, ex), 0, None


def insert_one(collection, cls, obj, primary_key=None):
    d = pb_to_dict_converter(obj, primary_key)
    try:
        collection.insert_one(d)
        return Error.ok(), obj
    except Exception as ex:
        logging.error(
            'failed to insert {} object to MongoDB, data is {}, exception is {}'.format(cls, d, ex))
        traceback.print_exc()
        return Error(Error.UNKNOWM, ex)


def update_one(collection, cls, obj, primary_key=None):
    d = pb_to_dict_converter(obj, primary_key)

    try:
        collection.update_one({'_id': d['_id']}, {'$set': d})
        return Error.ok()
    except Exception as ex:
        logging.error(
            'failed to update {} object to MongoDB, data is {}, exception is {}'.format(cls, d, ex))
        traceback.print_exc()
        return Error(Error.UNKNOWM, ex)
