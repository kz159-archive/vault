from endpoints import *


def setup_routes(app):
    app.router.add_get('/yt', get_yt, name='get_yt')
    app.router.add_get('/ig', get_ig, name='get_ig')
    app.router.add_post('/yt/store', post_yt_store, name='post_yt_store')
    app.router.add_post('/yt/update', post_yt_update, name='post_yt_update')
    app.router.add_post('/proxy', post_proxy, name='post_proxy')
    app.router.add_post('/ig/store', post_ig_store, name='post_ig_store')
    app.router.add_post('/ig/update', post_ig_update, name='post_ig_update')

