import logging

from sqlalchemy import DateTime, create_engine, Table, Column, Integer, String, MetaData
from alembic.config import Config

logger = logging.getLogger(__name__)

metadata = MetaData()
user_table = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('telegram_username', String),
    Column('access_level', Integer),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
)

class UserRepository():
    def __init__(self):
        config = Config("alembic.ini")
        self.engine = create_engine(config.get_main_option("sqlalchemy.url"))
    
    def get_by_id(self, id):
        try:
            with self.engine.connect() as conn:
                select_stmt = user_table.select().where(user_table.c.id == id)
                result = conn.execute(select_stmt)
                for row in result:
                    return row
        except Exception as e:
            logger.error(f'Failed to get user from db: {e}')
            return None
        
if __name__ == '__main__':
    # Query the 'user' table and print the results
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    ans =  UserRepository().get_by_id(0)
    print(ans)