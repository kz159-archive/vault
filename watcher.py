from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from helpers import get_db_dsn
from meta import YtApiKey

ENGINE = create_engine(get_db_dsn, echo=True)
SESSION_FACTORY = sessionmaker(bind=ENGINE)

while True:
    # Чекнуть базы на не наличие поля прокси
    # Представить прокси как словарь и
    # в него заполнять данные если отсутствуют
    pass