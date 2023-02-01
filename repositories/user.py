import sqlite3
from typing import Tuple

conn = sqlite3.connect('data/muninn.db')

class User ():
    def __init__(self, id, telegram_username, allowed, ):
        self.telegram_username = telegram_username
        self.allowed = allowed
        self.id = id

def get_user_from_db(username: str) -> User:
    try:
        c = conn.cursor()
        c.execute('SELECT id, telegram_username, allowed FROM users WHERE telegram_username = ?', (username,))
        result =  c.fetchone()
        print(result)
        return User(*result)
    except Exception as e:
        print(f'Failed to get user from db: {e}')
        return None