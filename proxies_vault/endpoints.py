"""
module describes route for web app
"""
from capturica_db.models import *

from helpers import *
from aiohttp import web


async def get_free_ig_session(request: web.Request) -> web.Response:
    """
    Получение инстаграм сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    # user_id = await check_authorized(request)
    sql_query = (sa.select([
        ig_session.c.ig_session_id,
        ig_session.c.login,
        ig_session.c.password,
        proxy.c.ip,
        proxy.c.port,
    ])
                 .select_from(ig_session
                              .join(proxy, ig_session.c.proxy_id == proxy.c.proxy_id)
                              )
                 .where(ig_session.c.is_used == False)
                 .limit(1)
                 )

    async with request.app['server'].db_connection() as connection:
        result = await (await connection.execute(sql_query)).fetchall()

    if not result:
        return web.json_response(data={}, status=400)

    result = parse_results(result)[0]

    update_query = (ig_session
             .update()
             .where(ig_session.c.ig_session_id == result['ig_session_id'])
             .values(is_used=True, last_used=datetime.now())
             .returning(ig_session.c.ig_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()

    return web.json_response(data=result, status=200)

async def free_ig_session(request: web.Request) -> web.Response:
    """
    Освобождение инстаграм сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    # user_id = await check_authorized(request)
    influencer_id = request.match_info['ig_session_id']

    update_query = (ig_session
             .update()
             .where(ig_session.c.ig_session_id == influencer_id)
             .values(is_used=False)
             .returning(ig_session.c.ig_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()

    return web.json_response(data='ok', status=200)

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
# async def post_proxy(request: web.Request) -> web.Response:
#     """
#     function that gets
#     proxy from posted json
#     """
#     try:
#         data = await request.json()
#         data = ProxyValid(**data)
#     except (JSONDecodeError, ValidationError):
#         return web.json_response(data={'ты': 'не прав'})
#
#     store_proxy(data)
#
#     return web.json_response({'status':'ok'})
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
# async def post_ig_store(request: web.Request) -> web.Response:
#     """
#     function gets ig creds from
#     request and stores it in db
#     """
#     try:
#         data = await request.json()
#         data = IgSessionStore(**data)
#     except (JSONDecodeError, ValidationError):
#         return web.json_response(data={'Ты':'не прав'})
#
#     row = store_ig_session(data)
#     if row:
#         return web.json_response({'status':'ok',
#                                   'session_id': row})
#
#     return web.json_response({"status":"error",
#                               "message":"NO_PROXY_AVAIL"}, status=502)
#
# async def post_ig_update(request: web.Request) -> web.Response:
#     """
#     update ig session using session id
#     """
#     try:
#         data = await request.json()
#         data = IgSessionUpdate(**data)
#     except (JSONDecodeError, ValidationError):
#         return web.json_response(data={'Ты':'не прав'})
#     if update_ig_session_status(data):
#         return web.Response()
#     return web.HTTPError()
