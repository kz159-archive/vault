from os import getenv

DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASSWORD = getenv('DB_PASSWORD', 'password')

DB_DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_USER}'
