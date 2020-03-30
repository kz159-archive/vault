"""
module for describing tables in sa and
pydantic basemodels
"""
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

ENGINE = create_engine('postgresql://postgres:password@localhost:5432',
                       echo=True)

BASE = declarative_base()

class Proxy(BASE):
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
    status = Column(String) # Ready, Unavailable, Banned, On_Delete


class YtApiKey(BASE):
    """
    youtube keys with status
    """
    __tablename__ = 'youtube_keys'
    key_id = Column(Integer, primary_key=True)
    proxy_id = Column(String)
    key = Column(String)
    status = Column(String, default="Ready") # Ready, Banned
    status_timestamp = Column(TIMESTAMP)

class IgSession(BASE):
    """
    instagram sessions
    """
    __tablename__ = 'instagram_sessions'
    session_id = Column(Integer, primary_key=True)
    session_name = Column(String)
    session_pass = Column(String)
    proxy_id = Column(String, primary_key=True)

class ProxyValid(BaseModel):
    """
    Proxy validation for DTO
    """
    address: str
    port: str
    user: str
    password: str


class YtApiKeyValid(BaseModel):
    """
    YouTube validation for DTO
    """
    key: str


class IgSessionValid(BaseModel):
    """
    Instagram validation for DTO
    """
    session_name: str
    session_pass: str


class Instruction:
    """
    class for storing instructions
    КЛАСС ПОД ВОПРОСОМ
    """
    beg = 'Для отправки запроса используйте curl\n'

    yt = f"""{beg}ютуб инструкция """
    ig = f"""{beg}ig instruction """
    proxy = f"""{beg}proxy instruction """

validations = {'proxy': ProxyValid,
               'ig': IgSessionValid,
               'yt': YtApiKeyValid}

BASE.metadata.create_all(ENGINE)
