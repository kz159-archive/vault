'''
helpers module which contains functions to work with dB
'''
from datetime import datetime
from json import JSONDecodeError

from pydantic import ValidationError
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from meta import YtApiKey, Proxy, IgSession, validations
from config import DB_DSN

ENGINE = create_engine(DB_DSN, echo=True)
SESSION_FACTORY = sessionmaker(bind=ENGINE)


def store_yt_key(key): # "with" or "session" style?
    """
    Store yotube api key in db
    """
    time = datetime.utcnow()
    session = SESSION_FACTORY()
    avail_proxy = session.query(Proxy).filter_by(key_id=None).first()
    if avail_proxy:
        yt = YtApiKey(key=key,
                      proxy_id=avail_proxy.proxy_id,
                      status_timestamp=time)
        session.add(yt)
        session.commit()  # RE DO Что если ключ будет доступен а прокси еще нет?
        avail_proxy.key_id = yt.key_id
        session.commit()
        return yt.key_id
    else:
        return None

def store_proxy(proxy):
    queue = Proxy.__table__.insert().values(address=proxy.address,
                                            port=proxy.port,
                                            user=proxy.user,
                                            password=proxy.password)
    with ENGINE.connect() as conn:
        conn.execute(queue)

def store_ig_session(ig):
    queue = IgSession.__table__.insert().values(session_name=ig.session_name,
                                                session_pass=ig.session_pass)
    with ENGINE.begin() as conn:
        conn.execute(queue)

def get_free_yt_meta():
    time = datetime.utcnow()
    statement = ('SELECT yt_key.key_id, key, address, port, "user", password'
                 " FROM yt_key "
                 "INNER JOIN proxy on proxy.key_id = yt_key.key_id "
                 "where status='Ready' or "
                 "(status='Banned' and status_timestamp "
                 "< NOW() - INTERVAL '25 hours') "
                 "order by status_timestamp;") # Преобразовать в sqlalchemy query
    with ENGINE.connect() as con:
        result = con.execute(statement).fetchone()
        con.execute(update(YtApiKey).\
            where(YtApiKey.key_id==result.key_id).\
            values(status='Locked', status_timestamp=time))
        return result

def get_proxy_(proxy_id):
    session = SESSION_FACTORY()
    queue = session.query(Proxy).filter_by(proxy_id=proxy_id).fetchone()
    session.close()
    return queue

async def check_json(request, service):
    """
    returns data if request is good
    """
    try:
        data = await request.json()
        data = validations[service](**data)
    except (JSONDecodeError, ValidationError):
        return None
    return data
