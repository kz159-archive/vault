"""
module describes route for web app
"""
from json import JSONDecodeError

from aiohttp import web
from pydantic import ValidationError

from helpers import (get_free_ig_meta, get_free_yt_meta,
                     store_ig_session, store_proxy, store_yt_key,
                     update_yt_key_status, get_proxy_)
from meta import Instruction, YtApiKeyValid, ProxyValid


async def get_yt(request):
    """
    get method for getting youtube metadata
    """
    try:
        data = dict(get_free_yt_meta().items())
        proxy = dict(get_proxy_(data['proxy_id'])) # without join
        data.update(proxy)
    except AttributeError:
        data = {'status': 'NO_KEYS_AVAILABLE'}
    return web.json_response(data=data)

async def get_ig(request):
    try:
        data = dict(get_free_ig_meta().items())
    except AttributeError:
        data = {'status': 'NO_SESSIONS_AVAILABLE'}
    return web.json_response(data=data)


async def post_proxy(request):
    """
    function that gets
    proxy from posted json
    """
    try:
        data = await request.json()
        data = ProxyValid(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'ты': 'не прав'})

    store_proxy(data)

    return web.json_response({'status':'ok'})

async def post_yt(request):
    """
    function that gets and
    updates yt keys in db
    """
    try:
        data = await request.json()
        data = YtApiKeyValid(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'ты': 'не прав'})

    if data.action == 'store':
        row = store_yt_key(data.key)
        if row:
            return web.json_response({'status':'ok',
                                      'key_id': row})

    elif data.action == 'update':
        if update_yt_key_status(data.key, data.status):
            return web.Response()
        return web.HTTPError()

    return web.json_response({"status":"error",
                              "message":"NO_PROXY_AVAIL"}, status=502)

async def post_ig(request):
    """
    function gets ig creds from
    request and stores it in db
    """
    data = await check_json(request, service='ig')
    if not data:
        return web.Response(text=Instruction.ig, status=401)

    row = store_ig_session(data)
    if row:
        return web.json_response({'status':'ok',
                                  'session_id': row})

    return web.json_response({"status":"error",
                              "message":"NO_PROXY_AVAIL"}, status=502)

