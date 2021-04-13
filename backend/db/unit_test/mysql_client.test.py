import sys
import os

sys.path.append('E:\github\examOnline')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db.orm import UserOrm
from gen.proto.db_pb2 import User
from db.mysql_client import MysqlClient, create_or_get_mysql_client

_CONNECTION_PATTERN = (
    'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8')


def test():
    connection_url = _CONNECTION_PATTERN.format(user='root', password='1234', host='localhost', port='3306', db='test')
    print(connection_url)
    engine = create_engine(connection_url, echo=True)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    record = User()
    record.id = '2017'
    record.name = 'aaa'
    record.role = 0
    try:
        user = UserOrm(record)
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        print(e)

def test_mysql_client():
    client = create_or_get_mysql_client()
    user = client.get_user('admin', 'test', 123)
    print(user)

test_mysql_client()

