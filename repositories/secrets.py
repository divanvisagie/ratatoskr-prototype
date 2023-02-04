import logging
import sqlite3

conn = sqlite3.connect('data/muninn.db')
logger = logging.getLogger(__name__)

class Secret (object):
    def __init__(self, user_id, app_id, question, answer):
        self.user_id = user_id
        self.app_id = app_id
        self.question = question
        self.answer = answer


def get_app_secret_for_user(user_id: int, app_id: int, question: str) -> Secret:
    try:
        c = conn.cursor()
        c.execute('SELECT question, answer FROM secrets WHERE user_id = ? AND app_id = ? AND question = ?', (user_id, app_id, question))
        result = c.fetchone()
        return Secret(user_id, app_id, result[0], result[1])
    except:
        logger.error(f'Failed to get secret for user: {user_id} and app: {app_id}')
        return None

def save_secret(secret: Secret):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO secrets (user_id, app_id, question, answer) VALUES (?, ?, ?, ?)', (secret.user_id, secret.app_id, secret.question, secret.answer))
        conn.commit()
    except Exception as e:
        logger.error(f'Failed to save secret for user: {e}')