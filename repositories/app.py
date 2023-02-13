
import logging
import sqlite3
from repositories.repository import Repository


conn = sqlite3.connect('data/muninn.db')
logger = logging.getLogger(__name__)


class AppRepository(Repository):
    
        def get_by_id(self, id):
            """Get the item by Id"""
            pass
    
        def save(self, id, item):
            """Save the item"""
            pass

        
        def get_id_by_name(self, app_name: str) -> int:
            try:
                c = conn.cursor()
                c.execute('SELECT id FROM app WHERE app_name = ?', (app_name,))
                result = c.fetchone()
                return result[0]
            except Exception as e:
                logger.error(f'Failed to get app id for app name: {e}')
                return -1

        def save_app(self, app_name: str):
            try:
                c = conn.cursor()
                c.execute('INSERT INTO app (app_name) VALUES (?)', (app_name,))
                conn.commit()
                return
            except Exception as e:
                logger.error(f'Failed to save app for user: {e}')
                return