from abc import ABCMeta, abstractmethod
from app.common.dto.response import Response
from typing import Optional

class PromptController(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, user_content: Optional[dict] = None) -> Response:
        pass

    async def handle_async(self, user_content: Optional[dict] = None) -> Response:
        pass
