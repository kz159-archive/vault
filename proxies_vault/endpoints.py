"""
module describes route for web app
"""
from capturica_db.models import *

from helpers import *
from aiohttp import web
from datetime import datetime

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
        proxy.c.login,
        proxy.c.password,
    ])
                 .select_from(ig_session
                              .join(proxy, ig_session.c.proxy_id == proxy.c.proxy_id)
                              )
                 .where(ig_session.c.is_used == False)
                 .where(ig_session.c.is_blocked == False)
                 .order_by(ig_session.c.last_used)
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
    ig_session_id = request.match_info['ig_session_id']

    update_query = (ig_session
             .update()
             .where(ig_session.c.ig_session_id == ig_session_id)
             .values(is_used=False, last_used=datetime.now())
             .returning(ig_session.c.ig_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()

    return web.json_response(data='ok', status=200)

async def get_free_yt_session(request: web.Request) -> web.Response:
    """
    Получение yt сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    # user_id = await check_authorized(request)
    sql_query = (sa.select([
        yt_session.c.yt_session_id,
        yt_session.c.api_key,
        proxy.c.ip,
        proxy.c.port,
        proxy.c.login,
        proxy.c.password,
    ])
                 .select_from(yt_session
                              .join(proxy, yt_session.c.proxy_id == proxy.c.proxy_id)
                              )
                 .where(yt_session.c.is_used == False)
                 .where(yt_session.c.is_blocked == False)
                 .order_by(yt_session.c.last_used)
                 .limit(1)
                 )

    async with request.app['server'].db_connection() as connection:
        result = await (await connection.execute(sql_query)).fetchall()

    if not result:
        return web.json_response(data={}, status=400)

    result = parse_results(result)[0]

    update_query = (yt_session
             .update()
             .where(yt_session.c.yt_session_id == result['yt_session_id'])
             .values(is_used=True, last_used=datetime.now())
             .returning(yt_session.c.yt_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()

    return web.json_response(data=result, status=200)

async def free_yt_session(request: web.Request) -> web.Response:
    """
    Освобождение инстаграм сессии
    :param request: web.Request
        Опциональные параметры:

    :return: web.Response
    """
    # user_id = await check_authorized(request)
    yt_session_id = request.match_info['yt_session_id']

    update_query = (yt_session
             .update()
             .where(yt_session.c.yt_session_id == yt_session_id)
             .values(is_used=False, last_used=datetime.now())
             .returning(yt_session.c.yt_session_id))

    async with request.app['server'].db_connection() as connection:
        updated = await (await connection.execute(update_query)).fetchall()

    return web.json_response(data='ok', status=200)


