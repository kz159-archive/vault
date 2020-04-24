from endpoints import *


def setup_routes(app):
    app.router.add_get('/ig', get_free_ig_session, name='get_free_ig_session')
    app.router.add_get('/ig/release/{ig_session_id:\d+}', free_ig_session, name='free_ig_session')
    app.router.add_get('/ig/block/{ig_session_id:\d+}', block_ig_session, name='block_ig_session')
    app.router.add_post('/ig/store', store_ig_session, name='post_ig_store')
    app.router.add_post('/proxy', post_proxy, name='post_proxy')

    # app.router.add_get('/yt', get_yt, name='get_yt')
    # app.router.add_post('/yt/store', post_yt_store, name='post_yt_store')
    # app.router.add_post('/yt/update', post_yt_update, name='post_yt_update')
    # app.router.add_post('/ig/update', post_ig_update, name='post_ig_update')
