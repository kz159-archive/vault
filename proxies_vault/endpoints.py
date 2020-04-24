"""
module describes route for web app
"""
from capturica_db.models import ig_session, proxy, sa

from helpers import *
from aiohttp import web
from datetime import datetime, timedelta

async def get_free_ig_session(request: web.Request) -> web.Response:
    """
    Получение инстаграм сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    day_ago = datetime.utcnow() + timedelta(hours=25)
    result = {}

    joined_tables = sa.join(ig_session, proxy,
                            ig_session.c.proxy_id == proxy.c.proxy_id)

    where = (((ig_session.c.is_used == False) & (ig_session.c.is_blocked == False)) |
             ((ig_session.c.is_blocked == True) & (ig_session.c.last_used < day_ago)))
    select_statement = (sa.select([ig_session.c.ig_session_id])
                        .where(where).limit(1))

    session_id = ig_session.c.ig_session_id.in_(select_statement)

    update_query = (ig_session
                    .update()
                    .where(session_id)
                    .values(is_used=True,
                            last_used=datetime.now(),
                            is_blocked=False)
                    .returning(ig_session.c.ig_session_id))

    async with request.app['server'].db_connection() as con:
        updated = await (await con.execute(update_query)).fetchall()
        if updated:
            result = parse_results(updated)[0]
            out = sa.select(([ig_session.c.ig_session_id,
                              ig_session.c.login,
                              ig_session.c.password,
                              proxy.c.ip,
                              proxy.c.port
                              ]).select_from(joined_tables).
                            where(ig_session.c.ig_session_id ==
                                  result['ig_session_id']))

            result = await (await con.execute(out)).fetchall()
            result = parse_results(result)[0]
    return web.json_response(data=result, status=200)

async def free_ig_session(request: web.Request) -> web.Response:
    """
    Освобождение инстаграм сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    influencer_id = request.match_info['ig_session_id']

    update_query = (ig_session
                    .update()
                    .where(ig_session.c.ig_session_id == influencer_id)
                    .values(is_used=False)
                    .returning(ig_session.c.ig_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()
    
    result = parse_results(updated)

    return web.json_response(data=result, status=200)

async def store_ig_session(request: web.Request) -> web.Response:
    """
    Добавление инстаграм сессий в базу данных
    TODO avail_proxy хардкод, необходимо реализовать логику
    "Если есть свободные прокси(считай без ключей ссылающихся на прокси)
    то добавить, иначе плюнуть ошибку"
    """
    data = await check_req(request, 'ig_session')

    avail_proxy = 1

    async with request.app['server'].db_connection() as con:
        insert_ig_session = (ig_session.insert()
                             .values(proxy_id=avail_proxy, **data))
        result = await (await con.execute(insert_ig_session)).scalar()

    return web.json_response({"status":"ok",
                              "ig_session_id":result})

async def post_proxy(request: web.Request) -> web.Response:
    """
    function that gets
    proxy from posted json
    """
    data = await check_req(request, 'proxy')
    print(data)

    insert_proxy = proxy.insert().values(**data)
    async with request.app['server'].db_connection() as con:
        res = await (await con.execute(insert_proxy)).scalar()

    return web.json_response({'status':'ok',
                              'res':res})

async def block_ig_session(request: web.Request) -> web.Response:
    """
    update ig session using session id
    """
    influencer_id = request.match_info['ig_session_id']
    
    block_session = (ig_session.update()
                     .values(is_blocked=True)
                     .where(ig_session.c.ig_session_id==influencer_id)
                    )

    async with request.app['server'].db_connection() as con:
        await con.execute(block_session)
    return web.Response()

# async def get_yt(request: web.Request) -> web.Response:
#     """
#     get method for getting youtube metadata
#     """
#     try:
#         data = dict(get_free_yt_meta().items())
#     except AttributeError:
#         data = {'status': 'NO_KEYS_AVAILABLE'}
#     return web.json_response(data=data)
#

#
#
# async def post_yt_store(request: web.Request) -> web.Response:
#     """
#     function that gets and
#     updates yt keys in db
#     """
#     try:
#         data = await request.json()
#         data = YtApiKeyStore(**data)
#     except (JSONDecodeError, ValidationError):
#         return web.json_response(data={'ты': 'не прав'})
#
#     row = store_yt_key(data.key)
#     if row:
#         return web.json_response({'status':'ok',
#                                   'key_id': row})
#
#     return web.json_response({"status":"error",
#                               "message":"NO_PROXY_AVAIL"}, status=502)
#
# async def post_yt_update(request: web.Request) -> web.Response:
#     """
#     function that updates yt meta
#     """
#     try:
#         data = await request.json()
#         data = YtApiKeyUpdate(**data)
#     except (JSONDecodeError, ValidationError):
#         return web.json_response(data={'ты': 'не прав'})
#
#     if update_yt_key_status(data):
#         return web.Response()
#     return web.HTTPBadRequest()
#

