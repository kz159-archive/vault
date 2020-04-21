"""
module describes route for web app
"""
from json import JSONDecodeError

from aiohttp import web
from pydantic import ValidationError

from proxies_vault.helpers import (get_free_ig_meta, get_free_yt_meta, store_ig_session,
                                   store_proxy, store_yt_key, update_ig_session_status,
                                   update_yt_key_status)
from proxies_vault.meta import (IgSessionStore, IgSessionUpdate, ProxyValid,
                                YtApiKeyStore, YtApiKeyUpdate)

def setup_routes(app):
    app.router.add_get('/yt', get_yt, name='get_yt')
    app.router.add_get('/ig', get_ig, name='get_ig')
    app.router.add_post('/yt/store', post_yt_store, name='post_yt_store')
    app.router.add_post('/yt/update', post_yt_update, name='post_yt_update')
    app.router.add_post('/proxy', post_proxy, name='post_proxy')
    app.router.add_post('/ig/store', post_ig_store, name='post_ig_store')
    app.router.add_post('/ig/update', post_ig_update, name='post_ig_update')

async def get_yt(request):
    """
    get method for getting youtube metadata
    """
    try:
        data = dict(get_free_yt_meta().items())
    except AttributeError:
        data = {'status': 'NO_KEYS_AVAILABLE'}
    return web.json_response(data=data)

async def get_ig(request):
    """
    get method for getting instagram meta
    """
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

async def post_yt_store(request):
    """
    function that gets and
    updates yt keys in db
    """
    try:
        data = await request.json()
        data = YtApiKeyStore(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'ты': 'не прав'})

    row = store_yt_key(data.key)
    if row:
        return web.json_response({'status':'ok',
                                  'key_id': row})

    return web.json_response({"status":"error",
                              "message":"NO_PROXY_AVAIL"}, status=502)

async def post_yt_update(request):
    """
    function that updates yt meta
    """
    try:
        data = await request.json()
        data = YtApiKeyUpdate(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'ты': 'не прав'})

    if update_yt_key_status(data):
        return web.Response()
    return web.HTTPBadRequest()

async def post_ig_store(request):
    """
    function gets ig creds from
    request and stores it in db
    """
    try:
        data = await request.json()
        data = IgSessionStore(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'Ты':'не прав'})

    row = store_ig_session(data)
    if row:
        return web.json_response({'status':'ok',
                                  'session_id': row})

    return web.json_response({"status":"error",
                              "message":"NO_PROXY_AVAIL"}, status=502)

async def post_ig_update(request):
    """
    update ig session using session id
    """
    try:
        data = await request.json()
        data = IgSessionUpdate(**data)
    except (JSONDecodeError, ValidationError):
        return web.json_response(data={'Ты':'не прав'})
    if update_ig_session_status(data):
        return web.Response()
    return web.HTTPError()