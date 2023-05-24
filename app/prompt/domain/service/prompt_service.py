from abc import ABCMeta, abstractmethod
from app.prompt.domain.model.prompt import Prompt

class PromptService(metaclass=ABCMeta):
    @abstractmethod
    def create_prompt(self) -> Prompt:
        pass
