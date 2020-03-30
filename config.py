from os import getenv

DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASSWORD = getenv('DB_PASSWORD', 'password')
