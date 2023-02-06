import logging
import sqlite3
from typing import List, Tuple

conn = sqlite3.connect('data/muninn.db')
logger = logging.getLogger(__name__)

class QAPair ():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

def get_history_for_user(user_id: int) -> List[QAPair]:
    print(f'Getting history for user: {user_id}')
    try:
        """Returns the first 10 entries from the history table for the given user"""
        c = conn.cursor()
        c.execute('SELECT question, answer FROM history WHERE user_id = ? LIMIT 10', (user_id,))
        result =  c.fetchall()
        return [QAPair(*row) for row in result]
    except Exception as e:
        logger.error(f'Failed to get history for user: {e}')
        return []

def get_last_answer(user_id: int) -> str:
    try:
        c = conn.cursor()
        c.execute('SELECT answer FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,))
        result = c.fetchone()
        return result[0]
    except Exception as e:
        logger.error(f'Failed to get last answer for user: {e}')
        return ''

def get_last_pair(user_id: int) -> QAPair:
    try:
        c = conn.cursor()
        c.execute('SELECT question, answer FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,))
        result = c.fetchone()
        return QAPair(*result)
    except Exception as e:
        logger.error(f'Failed to get last pair for user: {e}')
        return None

def save_history_for_user(user_id: int, pair: QAPair):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO history (user_id, question, answer) VALUES (?, ?, ?)', (user_id, pair.question, pair.answer))
        conn.commit()
        return
    except Exception as e:
        logger.error(f'Failed to save history for user: {e}')
        return

def save_app(app_name: str):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO app (app_name) VALUES (?)', (app_name,))
        conn.commit()
        return
    except Exception as e:
        logger.error(f'Failed to save app for user: {e}')
        return

def get_app_id_by_name(app_name: str) -> int:
    try:
        c = conn.cursor()
        c.execute('SELECT id FROM app WHERE app_name = ?', (app_name,))
        result = c.fetchone()
        return result[0]
    except Exception as e:
        logger.error(f'Failed to get app id for app name: {e}')
        return -1
   