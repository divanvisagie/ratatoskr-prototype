import datetime
import json
from typing import List
from bson import ObjectId
import pymongo

from language_model.base_model import AI_STOP_TOKEN, HUMAN_STOP_TOKEN
from log_factory.logger import create_logger

logger = create_logger(__name__)

class NewHistory ():
    def __init__(self, user_id: str, question: str, answer: str, responder: str = None):
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.answered_by = responder
        self.created_at = datetime.datetime.utcnow()
    
    def __dict__(self):
        return {
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'answered_by': self.answered_by,
            'created_at': self.created_at.isoformat(),
        }

class History ():
    def __init__(self, id, user_id, question, answer, created_at = datetime.datetime.utcnow()):
        self.id = id
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.created_at = created_at
    
    def __dict__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at,
        }

class HistoryRepository(object):
    def __init__(self):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["muninn"]
            self.collection = db["history"]
        except Exception as e:
            logger.error(f'Failed to connect to db: {e}')
    
    def get_by_id(self, id: str) -> List[History]:
        try:
            query = { "_id": ObjectId(id) }
            result = self.collection.find(query)
            history: List[History] = []
            for item in result:
                id = str(item['_id'])
                history.append(History(id, item['user_id'], item['question'], item['answer'], item['created_at']))
            return history
        except Exception as e:
            logger.error(f'Failed to get history from db: {e}')
            return None

    def get_last_n(self, user_id: str, n: int = 10) -> List[History]:
        try:
            query = { "user_id": user_id }
            result = self.collection.find(query).sort("created_at", -1).limit(n)
            history: List[History] = []
            for item in result:
                id = str(item['_id'])
                history.append(History(id, item['user_id'], item['question'], item['answer'], item['created_at']))
            return history
        except Exception as e:
            return None


    def save(self, item: NewHistory) -> str:
        """Save a history item for a user"""
        try:
            history_dict = json.loads(json.dumps(item.__dict__()))
            result = self.collection.insert_one(history_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f'Failed to save history item: {e}')
            return None
        
    def delete(self, id: str) -> bool:
        try:
            query = { "_id": ObjectId(id) }
            result = self.collection.delete_one(query)
            return result.deleted_count == 1
        except Exception as e:
            logger.error(f'Failed to delete history item: {e}')
            return False

def build_context_from_history(user_id: int) -> str:
    history_repository = HistoryRepository()
    context = history_repository.get_by_id(user_id)
    context_string = ''
    for qa in context:
        context_string += f'{HUMAN_STOP_TOKEN}: {qa.question}\n\n{AI_STOP_TOKEN}: {qa.answer}'
    return context_string
