import logging
import sqlite3
from typing import List, Tuple

from repositories.repository import Repository

conn = sqlite3.connect('data/muninn.db')
logger = logging.getLogger(__name__)

class History ():
    def __init__(self, question, answer, app_id = None):
        self.question = question
        self.answer = answer
        self.app_id = app_id

class HistoryRepository(Repository):
    
    def get_by_id(self, id: int, limit: int = 10) -> List[History]:
        """Get the item by Id"""
        logger.info(f'Getting history for user: {id}')
        try:
            """Returns the first 10 entries from the history table for the given user"""
            c = conn.cursor()
            c.execute(f'SELECT question, answer FROM history WHERE user_id = ? LIMIT {limit}', (id,))
            result =  c.fetchall()
            return [History(*row) for row in result]
        except Exception as e:
            logger.error(f'Failed to get history for user: {e}')
            return []

    def save(self, id: int, item: History):
        try:
            c = conn.cursor()
            c.execute('INSERT INTO history (user_id, question, answer) VALUES (?, ?, ?)', (id, item.question, item.answer))
            conn.commit()
            return
        except Exception as e:
            logger.error(f'Failed to save history for user: {e}')
            return
