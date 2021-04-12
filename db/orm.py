from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

from proto.db_pb2 import User

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
