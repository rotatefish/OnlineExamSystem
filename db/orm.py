from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

from proto.db_pb2 import User

_Base = declarative_base()


class UserOrm(_Base):
    __tablename__ = 'user'
    uid = Column(BigInteger, primary_key=True)
    name = Column(String)
    role = Column(Integer)
    password = Column(String)

    def __init__(self, record):
        super(UserOrm, self).__init__()
        self.uid = record.uid
        self.name = record.name
        self.role = record.role
        self.password = record.password

    def to_record(self):
        record = User()
        record.uid = self.uid
        record.name = self.name
        record.role = self.role
        record.password = self.password
        return record
