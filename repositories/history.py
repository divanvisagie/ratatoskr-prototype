import sqlite3
from typing import List, Tuple

conn = sqlite3.connect('data/muninn.db')

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
        print(f'Failed to get history for user: {e}')
        return []

def save_history_for_user(user_id: int, pair: QAPair):
    c = conn.cursor()
    c.execute('INSERT INTO history (user_id, question, answer) VALUES (?, ?, ?)', (user_id, pair.question, pair.answer))
    conn.commit()
    return