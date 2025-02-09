from abc import ABC, abstractmethod
from .conversation import Conversation
from typing import Dict, Any


class Tool(ABC):
    def __init__(self, name: str, terminating: bool = False):
        self.name = name
        self.terminating = terminating

    @abstractmethod
    def run(self, conversation: Conversation) -> str:
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        pass
