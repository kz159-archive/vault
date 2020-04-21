import aiopg.sa

from config import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASSWD


def get_connection_dsn(db_user, db_passwd, host, port, db_name):
    return f'postgresql://{db_user}:{db_passwd}@{host}:{port}/{db_name}'


async def init_db(app):
    engine = await aiopg.sa.create_engine(
        get_connection_dsn(DB_USER,
                           DB_PASSWD,
                           DB_HOST,
                           DB_PORT,
                           DB_NAME))
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()

