from abc import ABCMeta, abstractmethod
from app.prompt.domain.model.prompt import Prompt
from typing import Optional

class PromptService(metaclass=ABCMeta):
    @abstractmethod
    def create_prompt(self, user_content: Optional[dict] = None) -> Prompt:
        pass
