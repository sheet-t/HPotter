from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy_utils import IPAddressType

# https://www.ietf.org/rfc/rfc1700.txt
TCP = 6
UDP = 17

Base = declarative_base()

class ConnectionTable(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    sourceIP = Column(IPAddressType)
    sourcePort = Column(Integer)
    destIP = Column(IPAddressType)
    destPort = Column(Integer)
    proto = Column(Integer)

class CommandTable(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    extend_existing=True
    id = Column(Integer, primary_key=True)
    command = Column(String)
    connectiontable_id = Column(Integer, ForeignKey('connectiontable.id'))
    connectiontable = relationship("ConnectionTable")

class LoginTable(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    connectiontable_id = Column(Integer, ForeignKey('connectiontable.id'))
    connectiontable = relationship("ConnectionTable")

class HTTPTable(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    request = Column(String)

    connectiontable_id = Column(Integer, ForeignKey('connectiontable.id'))
    connectiontable = relationship("ConnectionTable")

