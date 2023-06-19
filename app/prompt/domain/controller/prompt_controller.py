from abc import ABCMeta, abstractmethod
from app.common.dto.response import Response
from typing import Optional

class PromptController(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, user_content: Optional[dict] = None) -> Response:
        pass

    @abstractmethod
    async def handle_async(self, user_content: Optional[dict] = None) -> Response:
        pass

    @abstractmethod
    def get_prompt_sample(self) -> str:
        pass
