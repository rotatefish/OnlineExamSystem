import functools
import threading
import traceback
import logging
import time
import json
import sqlalchemy

from collections import defaultdict
from db import mysql_helper as helper
from db.orm import UserOrm
from proto.db_pb2 import User


logging.basicConfig(level=logging.DEBUG)


__LOCK = threading.Lock()
__MYSQL_CLIENT = None
__MYSQL_CLIENT_READ_ONLY = None

__MYSQL_CONF = {
    'db_name': 'test',
    'write_host': 'localhost',
    'write_port': '3306',
    'write_user': 'root',
    'write_password': '1234',
}


def create_or_get_mysql_client():
    """
    if mysql client is exist, return it, else create a new mysql client

    """

    global __MYSQL_CLIENT, __LOCK
    if not __MYSQL_CLIENT:
        try:
            __LOCK.acquire()
            if not __MYSQL_CLIENT:
                __MYSQL_CLIENT = MysqlClient(
                    db_name=__MYSQL_CONF['db_name'],
                    host=__MYSQL_CONF['write_host'],
                    port=__MYSQL_CONF['write_port'],
                    user=__MYSQL_CONF['write_user'],
                    password=__MYSQL_CONF['write_password'],
                    connect_pool_size=20,
                    connect_pool_recycle=1800,
                    connect_pool_max_overflow=20)
        finally:
            __LOCK.release()
    return __MYSQL_CLIENT


class ErrorCode(object):
    """
    Error code enum for mysql client
    """
    OK = 0
    UNKNOWN = 1
    NO_RESULT = 2
    MULTIPLE_RESULT = 3
    INTEGRITY_ERROR = 4
    PUSH_INTERRUPT = 5


class MysqlClientError(Exception):
    def __init__(self, error_code, message):
        super(MysqlClientError, self).__init__(message)
        self.error_code = error_code


def to_error_code(e):
    if isinstance(e, sqlalchemy.orm.exc.NoResultFound):
        return ErrorCode.NO_RESULT
    if isinstance(e, sqlalchemy.orm.exc.MultipleResultsFound):
        return ErrorCode.MULTIPLE_RESULT
    if isinstance(e, sqlalchemy.exc.IntegrityError):
        return ErrorCode.INTEGRITY_ERROR
    if isinstance(e, MysqlClientError):
        return e.error_code
    return ErrorCode.UNKNOWN


class MysqlClient(object):
    """
    thread safe mysql client with scope_session
    """

    def __init__(self, db_name, host, port, user, password,
                 connect_pool_size, connect_pool_recycle,
                 connect_pool_max_overflow):
        self.session_factory = helper.create_session_factory(
            db_name, host, port, user, password,
            connect_pool_size, connect_pool_recycle,
            connect_pool_max_overflow)

    def inject_session(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):

            def log_exc(e):
                logging.warning(
                    'Error at mysql client method {}: {}'.format(f.__name__, e))
                if args:
                    logging.warning('agrs: {}'.format(str(args)))
                if kwargs:
                    logging.warning('kwargs: {}'.format(str(kwargs)))
                code = to_error_code(e)
                if code == ErrorCode.UNKNOWN:
                    traceback.print_exc()
                return code

            auto_commit = True
            session = None
            if len(args) > 0 and isinstance(args[0], sqlalchemy.orm.session.Session):
                auto_commit = False
                session = args[0]
                args = args[1:]
            else:
                session = self.session_factory
            if auto_commit:
                try:
                    result = f(self, session, *args, **kwargs)
                    session.commit()
                    return ErrorCode.OK, result
                except Exception as e:
                    code = log_exc(e)
                    session.rollback()
                    return code, None
                finally:
                    session.close()
            else:
                try:
                    result = f(self, session, *args, **kwargs)
                    return ErrorCode.OK, result
                except Exception as e:
                    return log_exc(e), None
        return wrapper

    def return_void(f):

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            code, result = f(self, *args, **kwargs)
            return code
        return wrapper

    def return_tuple(num):
        def tuple_return_inner(f):
            @functools.wraps(f)
            def wrapper(self, *args, **kwargs):
                code, result = f(self, *args, **kwargs)
                if code == ErrorCode.OK:
                    return tuple([code] + list(result))
                else:
                    return tuple([code] + [None] * num)

            return wrapper

        return tuple_return_inner

    @inject_session
    def create_user(self, sess, uid, name, role, password):
        record = User()
        record.uid = uid
        record.name = name
        record.role = role
        record.password = password
        helper.create_row(sess, UserOrm(record))
        return record

    @inject_session
    def get_user_by_id(self, sess, uid):
        orm = sess.query(UserOrm).filter(UserOrm.uid == uid).one()
        return orm.to_record()
