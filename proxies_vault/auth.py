import sqlalchemy as sa
from aiohttp_security import AbstractAuthorizationPolicy
from gpn_db.models import backend_user
from gpn_db.models import permission as permission_table
from passlib.hash import sha1_crypt


class AuthorisationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, app):
        super().__init__()
        self.app = app

    async def authorized_userid(self, identity):
        async with self.app['server'].db_connection() as connection:
            where = sa.and_(backend_user.c.login == identity,
                            backend_user.c.is_active)
            query = backend_user.select().where(where)
            ret = await connection.scalar(query)
        return ret

    async def permits(self, identity, permission, context=None):
        async with self.app['server'].db_connection() as connection:
            where = sa.and_(backend_user.c.login == identity,
                            backend_user.c.is_active)
            query = backend_user.select().where(where)
            usr = await(await connection.execute(query)).fetchone()
            if usr is not None:
                usr_id = usr[0]
                is_superuser = usr[3]
                if is_superuser:
                    return True

                where = permission_table.c.user_id == usr_id
                query = permission_table.select().where(where)
                ret = await connection.execute(query)
                result = await ret.fetchall()
                if ret is not None:
                    for row in result:
                        if row.permission_name == permission:
                            return True
            return False


async def check_credentials(app, username, password):
    async with app['server'].db_connection() as connection:
        where = sa.and_(backend_user.c.login == username,
                        backend_user.c.is_active)
        query = backend_user.select().where(where)
        usr = await(await connection.execute(query)).fetchone()
        if usr is not None:
            passwd = usr[2]
            return sha1_crypt.verify(password, hash=passwd)
    return False
