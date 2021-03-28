from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

from proto.db_pb2 import User

_Base = declarative_base()


class UserOrm(_Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(Integer)

    def __init__(self, record):
        super(UserOrm, self).__init__()
        self.id = record.id
        self.name = record.name
        self.role = record.role

    def to_record(self):
        record = User()
        record.id = self.id
        record.name = self.name
        record.role = self.role
        return record
