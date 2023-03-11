import json
import logging
from bson import ObjectId

import pymongo

logger = logging.getLogger(__name__)

class NewSecret (object):
    def __init__(self, user_id, app_id, question, answer):
        self.user_id = user_id
        self.app_id = app_id
        self.question = question
        self.answer = answer

    def __dict__(self):
        return {
            'user_id': self.user_id,
            'app_id': self.app_id,
            'question': self.question,
            'answer': self.answer,
        }
    
class Secret (object):
    def __init__(self, id, user_id, app_id, question, answer):
        self.id = id
        self.user_id = user_id
        self.app_id = app_id
        self.question = question
        self.answer = answer

    def __dict__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'app_id': self.app_id,
            'question': self.question,
            'answer': self.answer,
        }

class SecretRepository(object):
    def __init__(self):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["muninn"]
            self.collection = db["secret"]
        except Exception as e:
            logger.error(f'Failed to connect to db: {e}')
    
    def get_by_id(self, id) -> Secret:
        try:
            query = { "_id": ObjectId(id) }
            result = self.collection.find(query)
            for secret in result:
                id = str(secret['_id'])
                return Secret(id, secret['user_id'], secret['app_id'], secret['question'], secret['answer'])
        except Exception as e:
            logger.error(f'Failed to get secret from db: {e}')
            return None


    def save(self, secret: NewSecret) -> str:
        try:
            secret_dict = json.loads(json.dumps(secret.__dict__()))
            result = self.collection.insert_one(secret_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f'Failed to save secret for user: {e}')