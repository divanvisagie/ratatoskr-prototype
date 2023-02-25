import logging
import sqlite3

from confection import Config
from sqlalchemy import  DateTime, create_engine, Table, Column, Integer, String, MetaData, text
from alembic.config import Config
from repositories.repository import Repository

conn = sqlite3.connect('data/muninn.db')
logger = logging.getLogger(__name__)

metadata = MetaData()
secret_table = Table('secret', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('app_id', Integer, nullable=False),
    Column('question', String, nullable=False),
    Column('answer', String, nullable=False),
    Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP')),
    Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
)


class Secret (object):
    def __init__(self, user_id, app_id, question, answer):
        self.user_id = user_id
        self.app_id = app_id
        self.question = question
        self.answer = answer

       
class SecretRepository(object):
    def __init__(self):
        config = Config("alembic.ini")
        self.engine = create_engine(config.get_main_option("sqlalchemy.url"))
    
    def get_by_id(self, id):
        try:
            with self.engine.connect() as conn:
                select_stmt = secret_table.select().where(secret_table.c.id == id)
                result = conn.execute(select_stmt)
                for row in result:
                    return row
        except Exception as e:
            logger.error(f'Failed to get secret from db: {e}')
            return None

    def get_app_secret_for_user(self, user_id: int, app_id: int, question: str) -> Secret:
        try:
            with self.engine.connect() as conn:
                select_stmt = secret_table.select().where(
                    (secret_table.c.user_id == user_id) &
                    (secret_table.c.app_id == app_id) &
                    (secret_table.c.question == question)
                )
                result = conn.execute(select_stmt)
                for row in result:
                    logger.info(f'Found secret for user: {row}')
                    return row
        except Exception as e:
            logger.error(f'Failed to get secret from db: {e}')
            return None

    def save(self, secret: Secret):
        try:
            values = {
                'user_id': secret.user_id,
                'app_id': secret.app_id,
                'question': secret.question,
                'answer': secret.answer,
            }
            with self.engine.connect() as conn:
                insert_stmt = secret_table.insert().values(**values)
                result = conn.execute(insert_stmt)
                conn.commit()
                logger.info(f'Secret inserted: {result.rowcount}')
        except Exception as e:
            logger.error(f'Failed to save secret for user: {e}')