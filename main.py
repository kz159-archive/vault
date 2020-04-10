"""
Main launcher of app
"""
from aiohttp import web

from routes import (get_ig, get_yt, post_ig_store, post_ig_update, post_proxy,
                    post_yt_store, post_yt_update)

APP = web.Application()
APP.add_routes([web.get('/yt', get_yt),
                web.get('/ig', get_ig),
                web.post('/yt/store', post_yt_store),
                web.post('/yt/update', post_yt_update),
                web.post('/proxy', post_proxy),
                web.post('/ig/store', post_ig_store),
                web.post('/ig/update', post_ig_update)])

if __name__ == "__main__":
    print('ready')
    web.run_app(APP)
