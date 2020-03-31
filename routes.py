"""
module describes route for web app
"""
from aiohttp import web

from helpers import (check_json, get_free_yt_meta, store_ig_session,
                     store_proxy, store_yt_key, get_proxy_)
from meta import Instruction

async def get_yt(request):
    """
    get method for getting youtube metadata
    """
    data = get_free_yt_meta()
    return web.json_response(data=data)

async def post_yt(request):
    """
    function gets youtube key from
    request and stores it in db
    """
    data = await check_json(request, service='yt')
    if not data:
        return web.Response(text=Instruction.yt, status=401)

    store_yt_key(data.key)

    return web.json_response({'status':'ok'})

async def post_proxy(request):
    """
    function that gets
    proxy from posted json
    """
    data = await check_json(request, service='proxy')
    if not data:
        return web.Response(text=Instruction.proxy, status=401)

    store_proxy(data)

    return web.json_response({'status':'ok'})

async def get_proxy(request):
    """
    function that returns
    proxy info in json format
    """
    proxy_id = request.match_info.get('proxy_id')
    if not proxy_id:
        return web.Response(text=Instruction.proxy, status=401)
    proxy = get_proxy_(proxy_id)

    return web.json_response()

async def post_ig(request):
    """
    function gets ig creds from
    request and stores it in db
    """
    data = await check_json(request, service='ig')
    if not data:
        return web.Response(text=Instruction.ig, status=401)

    store_ig_session(data)

    return web.json_response({'status':'ok'})