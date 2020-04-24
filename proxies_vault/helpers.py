'''
helpers module which contains functions to work with dB
'''
# import csv
import datetime
# import io
import typing as tp
# import logging
#from datetime import datetime, timedelta
from json import JSONDecodeError

from aiohttp import web
from aiopg.sa.result import RowProxy
from pydantic import ValidationError, BaseModel

# import sqlalchemy as sa
# from sqlalchemy import create_engine, func, update
# from proxies_vault.meta import IgSession, Proxy, YtApiKey


# from multidict import MultiDict
# from xlsxwriter import Workbook
#
# from config import log


def parse_results(result: tp.List[RowProxy]) -> tp.List[tp.Dict]:
    json_result = []
    if result:
        for row in result:
            result_dict = {}
            for item in row:
                if isinstance(row[item], (datetime.datetime, datetime.date)):
                    result_dict[item] = row[item].isoformat()
                else:
                    result_dict[item] = row[item]
            json_result.append(result_dict)
    return json_result


class ProxyValid(BaseModel):
    ip: str
    port: str


class IgSession(BaseModel):
    login: str
    password: str


async def check_req(request, service) -> dict:
    validators = {'proxy':ProxyValid,
                  'ig_session':IgSession}
    try:
        data = await request.json()
        data = validators[service](**data)
    except (JSONDecodeError, ValidationError):
        raise web.HTTPBadRequest()
    return data.dict()

# def sentiment_match(sentiment=None):
#     sentiment_list = {
#         'positive': 'positive',
#         'negative': 'negative'
#     }
#
#     if sentiment:
#         try:
#             brand = sentiment_list[sentiment]
#         except KeyError:
#             log.error('Неверно указана тональность')
#             raise web.HTTPBadRequest(text='Неверно указана тональность')
#
#     return sentiment
#
#
# def brand_match(brand=None):
#     brand_list = {
#         'megafon': 'мегафон',
#         'beeline': 'билайн',
#         'mts': 'мтс',
#         'tele2': 'теле2'
#     }
#
#     if brand:
#         try:
#             brand = brand_list[brand]
#         except KeyError:
#             log.error('Неверно указан бренд')
#             raise web.HTTPBadRequest(text='Неверно указан бренд')
#
#     return brand
#
#
# def check_platform(platform):
#     platforms = ['youtube', 'instagram', 'all', None]
#
#     if platform not in platforms:
#         log.error('Неверно указана платформа')
#         raise web.HTTPBadRequest(text='Неверно указана платформа')
#
#
# def check_file_format(file_format):
#     existing_formats = ['xlsx', 'csv', None]
#
#     if file_format not in existing_formats:
#         log.error('Неверно указан формат файла')
#         raise web.HTTPBadRequest(text='Неверно указан формат файла')
#
#
# def csv_dict2bytes(data: tp.List[dict]):
#     """
#     Преобразует список словарей в BytesIO объект с представлением .csv файла
#
#     :param data: список словарей
#     :return: Битовый поток
#     """
#     sio = io.StringIO()
#     csv_writer = csv.writer(sio)
#
#     for i, data_item in enumerate(data):
#         if i == 0:
#             header = data_item.keys()
#             csv_writer.writerow(header)
#         csv_writer.writerow(data_item.values())
#     bio = io.BytesIO(sio.getvalue().encode('utf8'))
#     return bio
#
#
# def xlsx_dict2bytes(data: tp.List[dict]):
#     """
#     Преобразует список словарей в BytesIO объект с представлением .xlsx файла
#
#     :param data: список словарей
#     :return: Битовый поток
#     """
#     bio = io.BytesIO()
#     xlsx_workbook = Workbook(bio, {'in_memory': True})
#     xlsx_worksheet = xlsx_workbook.add_worksheet()
#
#     for row_count, data_item in enumerate(data):
#         if row_count == 0:
#             header = data_item.keys()
#             xlsx_worksheet.write_row(row=row_count, col=0, data=header)
#         xlsx_worksheet.write_row(row=row_count + 1, col=0,
#                                  data=data_item.values())
#     xlsx_workbook.close()
#     bio.seek(0)
#
#     return bio.read()
#
#
# def file_response(file_format, data, file_name):
#     if file_format == 'csv':
#         return web.Response(
#             headers=MultiDict({'Content-Disposition':
#                                    f'Attachment; filename={file_name}.csv',
#                                'Content-Type':
#                                    'text/csv'}),
#             body=csv_dict2bytes(data))
#     if file_format == 'xlsx':
#         return web.Response(
#             headers=MultiDict({
#                 'Content-Disposition': f'Attachment; filename={file_name}.xlsx',
#                 'Content-Type': 'application/'
#                                 'vnd.openxmlformats-officedocument'
#                                 '.spreadsheetml.sheet'}),
#             body=xlsx_dict2bytes(data))
#
#
# def store_yt_key(key): # "with" or "session" style?
#     """
#     Store yotube api key in db
#     """
#     session = SESSION_FACTORY()
#     avail_proxy = session.query(Proxy).filter_by(key_id=None).first()
#     if avail_proxy:
#         youtube_key = YtApiKey(key=key,
#                                proxy_id=avail_proxy.proxy_id,
#                                status_timestamp=func.now())
#         session.add(youtube_key)
#         session.commit()
#         avail_proxy.key_id = youtube_key.key_id
#         session.commit()
#         return youtube_key.key_id
#     else:
#         return None
#
# def store_ig_session(data):
#     """
#     store instagram session meta
#     """
#     session = SESSION_FACTORY()
#     avail_proxy = session.query(Proxy).filter_by(session_id=None).first()
#     if avail_proxy:
#         instagram_queue = IgSession(session_name=data.session_name,
#                                     session_pass=data.session_pass,
#                                     proxy_id=avail_proxy.proxy_id,
#                                     status_timestamp=func.now())
#         session.add(instagram_queue)
#         session.commit()
#         avail_proxy.session_id = instagram_queue.session_id
#         session.commit()
#         return instagram_queue.session_id
#     return None
#
# def store_proxy(proxy):
#     queue = Proxy.__table__.insert().values(address=proxy.address,
#                                             port=proxy.port,
#                                             user=proxy.user,
#                                             password=proxy.password)
#     with ENGINE.connect() as conn:
#         conn.execute(queue)
#
# def get_free_yt_meta():
#     now = datetime.utcnow()
#     day_ago = now + timedelta(hours=25)
#     j = sa.join(YtApiKey, Proxy, YtApiKey.proxy_id == Proxy.proxy_id)
#
#     where = (YtApiKey.status == 'Ready') | \
#             ((YtApiKey.status == 'Blocked') & \
#             (YtApiKey.status_timestamp < day_ago))
#     sel = sa.select([YtApiKey.key_id]).where(where).limit(1)
#     yt_id = YtApiKey.key_id.in_(sel)
#     upd_sttm = update(YtApiKey).values(status='Locked',
#                                        status_timestamp=func.now()).\
#          where(yt_id).returning(YtApiKey.key_id)
#
#     with ENGINE.begin() as con:
#         result = con.execute(upd_sttm).fetchone()
#         if result:
#             out = sa.select([YtApiKey.key_id,
#                              YtApiKey.key,
#                              Proxy.address,
#                              Proxy.user,
#                              Proxy.password,
#                              Proxy.port]).select_from(j).\
#                              where(YtApiKey.key_id == result.key_id)
#             result = con.execute(out).fetchone()
#     return result
#
# def get_free_ig_meta():
#     now = datetime.utcnow()
#     day_ago = now + timedelta(hours=25)
#     j = sa.join(IgSession, Proxy, IgSession.proxy_id == Proxy.proxy_id)
#
#     where = (IgSession.status == 'Ready') | \
#             ((IgSession.status == 'Blocked') & \
#             (IgSession.status_timestamp < day_ago))
#     sel_sttm = sa.select([IgSession.session_id]).where(where).limit(1)
#     ses_id = IgSession.session_id.in_(sel_sttm)
#     upd_sttm = update(IgSession).values(status='Locked',
#                                         status_timestamp=func.now()).\
#         where(ses_id).returning(IgSession.session_id)
#
#     with ENGINE.begin() as con:
#         result = con.execute(upd_sttm).fetchone()
#         if result:
#             out = sa.select([IgSession.session_id,
#                              IgSession.session_name,
#                              IgSession.session_pass,
#                              Proxy.address,
#                              Proxy.user,
#                              Proxy.password,
#                              Proxy.port]).select_from(j).\
#                              where(IgSession.session_id == result.session_id)
#             result = con.execute(out).fetchone()
#         return result
#
# def get_proxy_(proxy_id):
#     session = SESSION_FACTORY()
#     queue = session.query(Proxy).filter_by(proxy_id=proxy_id).first()
#     session.close()
#     return queue.as_dict()
#
# def update_yt_key_status(data):
#     session = SESSION_FACTORY()
#     yt_key = session.query(YtApiKey).filter_by(key_id=data.key_id).first()
#     if yt_key:
#         yt_key.status = data.status
#         yt_key.status_timestamp = func.now()
#         session.commit()
#         return True
#     logging.error(f'Theres something wrong with db, the key is {data.key_id}')
#     return False
#
# def update_ig_session_status(data):
#     session = SESSION_FACTORY()
#     ig_session = session.query(IgSession).\
#         filter_by(session_id=data.session_id).first()
#     if ig_session:
#         ig_session.status = data.status
#         ig_session.status_timestamp = func.now()
#         session.commit()
#         return True
#     logging.error(
#         f'Theres something wrong with db, the key is {data.session_id}')
#     return False
