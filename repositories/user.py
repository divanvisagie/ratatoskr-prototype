import logging
import json
import pymongo

logger = logging.getLogger(__name__)

class NewUser (object):
    def __init__(self, telegram_username, access_level):
        self.telegram_username = telegram_username
        self.access_level = access_level

    def __dict__(self):
        return {
            'telegram_username': self.telegram_username,
            'access_level': self.access_level
        }

class User (object):
    def __init__(self, id, telegram_username, access_level):
        self.id = id
        self.telegram_username = telegram_username
        self.access_level = access_level

    def __dict__(self):
        return {
            'id': self.id,
            'telegram_username': self.telegram_username,
            'access_level': self.access_level
        }


class UserRepository():
    def __init__(self):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["muninn"]
            self.collection = db["user"]
        except Exception as e:
            logger.error(f'Failed to connect to db: {e}')
    
    def get_by_id(self, id) -> User:
        try:
           query = { "id": id }
           result = self.collection.find(query)
           for user in result:
               id = str(user['_id'])
               return User(id, user['telegram_username'], user['access_level'])
        except Exception as e:
            logger.error(f'Failed to get user from db: {e}')
            return None
        
    def get_by_telegram_username(self, telegram_username) -> User:
        try:
           query = { "telegram_username": telegram_username }
           result = self.collection.find(query)
           for user in result:
               id = str(user['_id'])
               return User(id, user['telegram_username'], user['access_level'])
        except Exception as e:
            logger.error(f'Failed to get user from db: {e}')
            return None
        
    def save(self, user: NewUser) -> str:
        try:
            # Convert the User object to a dictionary
            user_dict = json.loads(json.dumps(user.__dict__()))
            result =  self.collection.insert_one(user_dict)
            result.inserted_id
        except Exception as e:
            logger.error(f'Failed to save user to db: {e}')
            return None
        
    def deleteByTelegramUsername(self, telegram_username):
        try:
            query = { "telegram_username": telegram_username }
            self.collection.delete_one(query)
        except Exception as e:
            logger.error(f'Failed to delete user from db: {e}')
            return None
       
        
if __name__ == '__main__':
    # Query the 'user' table and print the results
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )