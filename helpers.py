'''
helpers module which contains functions to work with dB
'''
import logging
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker

from config import DB_DSN
from meta import IgSession, Proxy, YtApiKey

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

def store_ig_session(ig):
    """
    store instagram session meta
    """
    session = SESSION_FACTORY()
    avail_proxy = session.query(Proxy).filter_by(session_id=None).first()
    if avail_proxy:
        instagram_queue = IgSession(session_name=ig.session_name,
                                    session_pass=ig.session_pass,
                                    proxy_id=avail_proxy.proxy_id,
                                    status_timestamp=func.now())
        session.add(instagram_queue)
        session.commit()
        avail_proxy.session_id = instagram_queue.session_id
        session.commit()
        return instagram_queue.session_id
    else:
        return None

def store_proxy(proxy):
    queue = Proxy.__table__.insert().values(address=proxy.address,
                                            port=proxy.port,
                                            user=proxy.user,
                                            password=proxy.password)
    with ENGINE.connect() as conn:
        conn.execute(queue)

def get_free_yt_meta():
    # update where yt api key returning
    now = datetime.utcnow()
    two_hours_ago = now + timedelta(hours=1)
    j = sa.join(YtApiKey, Proxy, YtApiKey.proxy_id == Proxy.proxy_id)

    where = (YtApiKey.status == 'Ready') | \
            ((YtApiKey.status == 'Blocked') & \
            (YtApiKey.status_timestamp < two_hours_ago))
    sel = sa.select([YtApiKey.key_id]).where(where).limit(1)
    yt_id = YtApiKey.key_id.in_(sel)
    upd_sttm = update(YtApiKey).values(status='Locked',
                                       status_timestamp=func.now()).\
         where(yt_id).returning(YtApiKey.key_id)

    with ENGINE.begin() as con:
        result = con.execute(upd_sttm).fetchone()
        if result:
            out = sa.select([YtApiKey.key,
                             Proxy.address,
                             Proxy.user,
                             Proxy.password,
                             Proxy.port]).select_from(j).\
                             where(YtApiKey.key_id == result.key_id)
            result = con.execute(out).fetchone()
    return result

def get_free_ig_meta():
    # Сначала мы выбираем прокси через update давая ему статус locked
    statеment = ('SELECT ig_session.session_id, session_name, session_pass, address, port, "user", password'
                 " FROM ig_session "
                 "INNER JOIN proxy on proxy.session_id = ig_session.session_id "
                 "where status='Ready' or "
                 "(status='Banned' and status_timestamp "
                 "< NOW() - INTERVAL '25 hours') "
                 "order by status_timestamp;")
    with ENGINE.connect() as con:
        result = con.execute(statеment).fetchone()
        con.execute(update(IgSession).\
            where(IgSession.session_id == result.session_id).\
            values(status='Locked', status_timestamp=func.now()))
        return result

def get_proxy_(proxy_id):
    session = SESSION_FACTORY()
    queue = session.query(Proxy).filter_by(proxy_id=proxy_id).first()
    session.close()
    return queue.as_dict()

def update_yt_key_status(key, status):
    session = SESSION_FACTORY()
    q = session.query(YtApiKey).filter_by(key=key).first()
    if q:
        q.status = status
        session.commit()
        return True
    logging.error(f'Theres something wrong with db, the key is {key}')
    return False

def release_ig_session(ses, status):
    session = SESSION_FACTORY()
    q = session.query(IgSession).filter_by(session_id=ses).first()
    if q:
        q.status = status
        session.commit()
        return True
    logging.error(f'Theres something wrong with db, the key is {ses}')
    return False
