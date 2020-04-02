from aiohttp import web 
from routes import get_yt, post_yt, post_proxy, post_ig, get_proxy


APP = web.Application()
APP.add_routes([web.get('/yt', get_yt),
                web.post('/yt', post_yt),
                web.post('/proxy', post_proxy),
                web.post('/ig', post_ig)])

if __name__ == "__main__":
    print('ready')
    web.run_app(APP)
