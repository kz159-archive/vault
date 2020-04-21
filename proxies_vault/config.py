import logging
import os

# логирование
logging.basicConfig(
    format='%(levelname)s - %(message)s'
)
log = logging.getLogger('capturica.webpage.backend')

log_level = os.getenv('LOGLEVEL', 'DEBUG')
assert log_level in ('CRITICAL', 'FATAL', 'ERROR', 'WARN',
                     'WARNING', 'INFO', 'DEBUG', 'NOTSET')

log.setLevel(log_level)
##

listen_port = int(os.getenv('SERVER_PORT', 80))

# подключение к БД
DB_USER = os.getenv('DB_USER', 'mrbot')
assert DB_USER

DB_PASSWD = os.getenv('DB_PASSWORD', 'vladandothers')

DB_HOST = os.getenv('DB_HOST', 'localhost')
assert DB_HOST

DB_PORT = os.getenv('DB_PORT', '2000')
assert DB_PORT

DB_NAME = os.getenv('DB_NAME', 'cap')
assert DB_NAME

log.info(f"Были получены следующие параметры конфигурации:\n"
         f"\tLOGLEVEL={log_level}\n"
         f"\tDATABASE_NAME={DB_NAME}\n"
         f"\tDATABASE_HOST={DB_HOST}\n"
         f"\tDATABASE_PORT={DB_PORT}\n"
         f"\tDATABASE_USER={DB_USER}\n"
         f"\tDATABASE_PASSWORD={DB_PASSWD}")
##
