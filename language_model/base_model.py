from abc import ABC, abstractmethod

HUMAN_STOP_TOKEN = "User"
AI_STOP_TOKEN = "Bot"

class BaseModel (ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass
