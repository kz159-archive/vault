"""
module for describing tables in sa and
pydantic basemodels
"""
from typing import Optional
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import (TIMESTAMP, Column, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base

from config import DB_DSN

ENGINE = create_engine(DB_DSN, echo=True)

BASE = declarative_base()

class Basev2(BASE):
    __abstract__ = True

    def as_dict(self):
        '''returns row object as dict'''
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Proxy(Basev2):
    '''
    proxy table with required metadata
    '''
    __tablename__ = 'proxy'
    proxy_id = Column(Integer, primary_key=True)
    key_id = Column(Integer)
    session_id = Column(Integer) # None, {session_id}
    address = Column(String)
    port = Column(Integer)
    user = Column(String)
    password = Column(String)
    #status = Column(String, default='Check_need') # Ready, Unavailable,
    #                                              # Banned, Checking


class YtApiKey(Basev2):
    """
    youtube keys with status
    """
    __tablename__ = 'yt_key'
    key_id = Column(Integer, primary_key=True)
    proxy_id = Column(Integer, default="1")
    key = Column(String)
    status = Column(String, default="Ready") # Ready, Banned, Locked
    status_timestamp = Column(TIMESTAMP)


class IgSession(Basev2):
    """
    instagram sessions
    """
    __tablename__ = 'ig_session'
    session_id = Column(Integer, primary_key=True)
    proxy_id = Column(Integer)
    session_name = Column(String)
    session_pass = Column(String)
    status = Column(String, default="Ready") # Ready, Banned, Locked
    status_timestamp = Column(TIMESTAMP)


class StatusEnum(str, Enum):
    ready = 'Ready'
    blocked = 'Blocked'


class ProxyValid(BaseModel):
    """
    Proxy validation for DTO
    """
    address: str
    port: str
    user: str
    password: str


class YtApiKeyStore(BaseModel):
    """
    YouTube key store validation for DTO
    """
    key: str


class YtApiKeyUpdate(BaseModel):
    """
    Youtube key status update validation
    """
    key_id: str
    status: StatusEnum

class IgSessionStore(BaseModel):
    """
    Instagram validation store check for DTO
    """
    session_name: str
    session_pass: str


class IgSessionUpdate(BaseModel):
    """
    Instagram validation updsate check
    """
    session_id: int
    status: StatusEnum


class Instruction:
    """
    class for storing instructions
    КЛАСС ПОД ВОПРОСОМ
    """
    beg = 'Для отправки запроса используйте curl\n'

    yt = f"""{beg}ютуб инструкция """
    ig = f"""{beg}ig instruction """
    proxy = f"""{beg}proxy instruction """

BASE.metadata.create_all(ENGINE) # Alembic?
