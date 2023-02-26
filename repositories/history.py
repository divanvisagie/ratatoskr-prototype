import logging
from typing import List, Tuple

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine, text

from repositories.repository import Repository
logger = logging.getLogger(__name__)

metadata = MetaData()
history_table = Table('history', metadata,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('user_id', Integer, nullable=False),
   Column('question', String, nullable=False),
   Column('answer', String, nullable=False),
   Column('answered_by', String, nullable=False),    
   Column('created_at', DateTime, server_default=text('CURRENT_TIMESTAMP')),
   Column('updated_at', DateTime, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))               
)

class NewHistory ():
    def __init__(self, question, answer, responder = None):
        self.question = question
        self.answer = answer
        self.answered_by = responder

    def __str__(self) -> str:
        return f'{self.question} - {self.answer} by {self.answered_by}'

class HistoryRepository(object):
    def __init__(self):
        try:
            self.engine = create_engine("postgresql://user:pass@localhost:5432/muninn")
        except Exception as e:
            logger.error(f'Failed to connect to db: {e}')
    
    def get_by_id(self, user_id: int, limit: int = 10) -> List[Tuple]:
        try:
            with self.engine.connect() as conn:
                select_stmt = history_table.select().where(
                    history_table.c.user_id == user_id
                ).order_by(
                    history_table.c.created_at.desc()
                ).limit(limit)
                result = conn.execute(select_stmt)
               
                history = [row for row in result]

                return list(reversed(history))
        except Exception as e:
            logger.error(f'Failed to get history from db: {e}')
            return None
            
    def delete_all(self, user_id: int):
        """Delete all history for a user"""
        try:
            with self.engine.connect() as conn:
                delete_stmt = history_table.delete().where(history_table.c.user_id == user_id)
                conn.execute(delete_stmt)
                conn.commit()
        except Exception as e:
            logger.error(f'Failed to delete history: {e}')

    def save(self, user_id: int, item: NewHistory):
        """Save a history item for a user"""
        try:
            with self.engine.connect() as conn:
                insert_stmt = history_table.insert().values(
                    user_id = user_id, 
                    question = item.question,
                    answer = item.answer, 
                    answered_by = item.answered_by
                )
                conn.execute(insert_stmt)
                conn.commit()
        except Exception as e:
            logger.error(f'Failed to save history item: {e}')

