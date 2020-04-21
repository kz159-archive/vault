'''
helpers module which contains functions to work with dB
'''
import logging
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker

from proxies_vault.config import DB_DSN
from proxies_vault.meta import IgSession, Proxy, YtApiKey

ENGINE = create_engine(DB_DSN, echo=True)
SESSION_FACTORY = sessionmaker(bind=ENGINE)

def store_yt_key(key): # "with" or "session" style?
    """
    Store yotube api key in db
    """
    session = SESSION_FACTORY()
    avail_proxy = session.query(Proxy).filter_by(key_id=None).first()
    if avail_proxy:
        youtube_key = YtApiKey(key=key,
                               proxy_id=avail_proxy.proxy_id,
                               status_timestamp=func.now())
        session.add(youtube_key)
        session.commit()
        avail_proxy.key_id = youtube_key.key_id
        session.commit()
        return youtube_key.key_id
    else:
        return None

def store_ig_session(data):
    """
    store instagram session meta
    """
    session = SESSION_FACTORY()
    avail_proxy = session.query(Proxy).filter_by(session_id=None).first()
    if avail_proxy:
        instagram_queue = IgSession(session_name=data.session_name,
                                    session_pass=data.session_pass,
                                    proxy_id=avail_proxy.proxy_id,
                                    status_timestamp=func.now())
        session.add(instagram_queue)
        session.commit()
        avail_proxy.session_id = instagram_queue.session_id
        session.commit()
        return instagram_queue.session_id
    return None

def store_proxy(proxy):
    queue = Proxy.__table__.insert().values(address=proxy.address,
                                            port=proxy.port,
                                            user=proxy.user,
                                            password=proxy.password)
    with ENGINE.connect() as conn:
        conn.execute(queue)

def get_free_yt_meta():
    now = datetime.utcnow()
    day_ago = now + timedelta(hours=25)
    j = sa.join(YtApiKey, Proxy, YtApiKey.proxy_id == Proxy.proxy_id)

    where = (YtApiKey.status == 'Ready') | \
            ((YtApiKey.status == 'Blocked') & \
            (YtApiKey.status_timestamp < day_ago))
    sel = sa.select([YtApiKey.key_id]).where(where).limit(1)
    yt_id = YtApiKey.key_id.in_(sel)
    upd_sttm = update(YtApiKey).values(status='Locked',
                                       status_timestamp=func.now()).\
         where(yt_id).returning(YtApiKey.key_id)

    with ENGINE.begin() as con:
        result = con.execute(upd_sttm).fetchone()
        if result:
            out = sa.select([YtApiKey.key_id,
                             YtApiKey.key,
                             Proxy.address,
                             Proxy.user,
                             Proxy.password,
                             Proxy.port]).select_from(j).\
                             where(YtApiKey.key_id == result.key_id)
            result = con.execute(out).fetchone()
    return result

def get_free_ig_meta():
    now = datetime.utcnow()
    day_ago = now + timedelta(hours=25)
    j = sa.join(IgSession, Proxy, IgSession.proxy_id == Proxy.proxy_id)

    where = (IgSession.status == 'Ready') | \
            ((IgSession.status == 'Blocked') & \
            (IgSession.status_timestamp < day_ago))
    sel_sttm = sa.select([IgSession.session_id]).where(where).limit(1)
    ses_id = IgSession.session_id.in_(sel_sttm)
    upd_sttm = update(IgSession).values(status='Locked',
                                        status_timestamp=func.now()).\
        where(ses_id).returning(IgSession.session_id)

    with ENGINE.begin() as con:
        result = con.execute(upd_sttm).fetchone()
        if result:
            out = sa.select([IgSession.session_id,
                             IgSession.session_name,
                             IgSession.session_pass,
                             Proxy.address,
                             Proxy.user,
                             Proxy.password,
                             Proxy.port]).select_from(j).\
                             where(IgSession.session_id == result.session_id)
            result = con.execute(out).fetchone()
        return result

def get_proxy_(proxy_id):
    session = SESSION_FACTORY()
    queue = session.query(Proxy).filter_by(proxy_id=proxy_id).first()
    session.close()
    return queue.as_dict()

def update_yt_key_status(data):
    session = SESSION_FACTORY()
    yt_key = session.query(YtApiKey).filter_by(key_id=data.key_id).first()
    if yt_key:
        yt_key.status = data.status
        yt_key.status_timestamp = func.now()
        session.commit()
        return True
    logging.error(f'Theres something wrong with db, the key is {data.key_id}')
    return False

def update_ig_session_status(data):
    session = SESSION_FACTORY()
    ig_session = session.query(IgSession).\
        filter_by(session_id=data.session_id).first()
    if ig_session:
        ig_session.status = data.status
        ig_session.status_timestamp = func.now()
        session.commit()
        return True
    logging.error(
        f'Theres something wrong with db, the key is {data.session_id}')
    return False
