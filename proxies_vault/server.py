from contextlib import asynccontextmanager
from typing import Optional, List

import aiohttp_session
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from auth import AuthorisationPolicy
from db import init_db, close_db
from routes import setup_routes


class Server:
    def __init__(self, port):
        self._app = web.Application()
        self._app.on_startup.extend([init_db])
        self._app.on_shutdown.extend([close_db])
        setup_routes(self._app)
        self.port = port

        aiohttp_session.setup(
            app=self._app,
            storage=EncryptedCookieStorage(
                secret_key=bytes([
                    0x4c, 0x06, 0x95, 0xe7, 0xcc, 0x5b, 0x28, 0xa1,
                    0x75, 0x70, 0xef, 0xca, 0x7b, 0x93, 0xc9, 0x14,
                    0x0c, 0xdd, 0x03, 0x42, 0x0d, 0xae, 0x27, 0x6c,
                    0xb7, 0xb2, 0xcf, 0x58, 0x20, 0xa2, 0xf8, 0xe7
                ])
            ))
        setup_security(self._app,
                       identity_policy=SessionIdentityPolicy(),
                       autz_policy=AuthorisationPolicy(self._app))

        self._app['server'] = self

    @staticmethod
    def setup_middlewares(middlewares: Optional[List] = ()):
        return middlewares

    @asynccontextmanager
    async def db_connection(self):
        async with self._app['db'].acquire() as connection:
            yield connection

    def run(self):
        web.run_app(self._app, port=self.port)
