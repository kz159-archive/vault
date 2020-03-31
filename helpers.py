'''
helpers module which contains functions to work with dB
'''
from datetime import datetime
from json import JSONDecodeError, loads

from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meta import YtApiKey, Proxy, IgSession, validations
from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, DB_DSN

ENGINE = create_engine(DB_DSN, echo=True)
SESSION_FACTORY = sessionmaker(bind=ENGINE)


def store_yt_key(key):
    """
    Store yotube api key in db
    """
    queue = YtApiKey.__table__.insert().values(key=key,
                                               status_timestamp=datetime.now())
    with ENGINE.begin() as conn:
        conn.execute(queue)

def store_proxy(proxy):
    queue = Proxy.__table__.insert().values(address=proxy.address,
                                            port=proxy.port,
                                            user=proxy.user,
                                            password=proxy.password)
    with ENGINE.begin() as conn:
        conn.execute(queue)

def store_ig_session(ig):
    queue = IgSession.__table__.insert().values(session_name=ig.session_name,
                                                session_pass=ig.session_pass)
    with ENGINE.begin() as conn:
        conn.execute(queue)

def get_free_yt_meta():
    session = SESSION_FACTORY()
    ll = session.query(YtApiKey).filter_by(status='Ready').first()
    session.close() # А если у нас ничего нет?
    return loads(ll.__dict__)

def get_proxy_(proxy_id):
    session = SESSION_FACTORY()
    queue = session.query(Proxy).filter_by(proxy_id)
    session.close()
    return queue.as_dict

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
