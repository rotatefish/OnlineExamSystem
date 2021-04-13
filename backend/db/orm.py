from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

from proto.db_pb2 import User
from proto.db_pb2 import Contest

_Base = declarative_base()


class UserOrm(_Base):
    __tablename__ = 'user'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    role = Column(Integer)
    email = Column(String)
    avatar = Column(String)
    gender = Column(Integer)
    password = Column(String)

    def __init__(self, record):
        super(UserOrm, self).__init__()
        self.user_id = record.user_id
        self.name = record.name
        self.role = record.role
        self.email = record.email
        self.avatar = record.avatar
        self.gender = record.gender
        self.password = record.password

    def to_record(self):
        record = User()
        record.user_id = self.user_id
        record.name = self.name
        record.role = self.role
        record.email = self.email
        record.avatar = self.avatar
        record.gender = self.gender
        record.password = self.password
        return record


class ContestOrm(_Base):
    __tablename__ = 'contest'
    cid = Column(Integer, primary_key=True)
    eid = Column(Integer)
    status = Column(Integer)
    begin_time = Column(BigInteger)
    finish_time = Column(BigInteger)
    created_by = Column(String)
    creation_time = Column(BigInteger)
    modified_time = Column(BigInteger)

    def __init__(self, record):
        super(UserOrm, self).__init__()
        self.cid = record.cid
        self.eid = record.eid
        self.status = record.status
        self.begin_time = record.begin_time
        self.finish_time = record.finish_time
        self.created_by = record.created_by
        self.creation_time = record.creation_time
        self.modified_time = record.modified_time
    
    def to_record(self):
        record = Contest()
        record.cid = self.cid
        record.eid = self.eid
        record.status = self.status
        record.begin_time = self.begin_time
        record.finish_time = self.finish_time
        record.created_by = self.created_by
        record.creation_time = self.creation_time
        record.modified_time = self.modified_time
        return record