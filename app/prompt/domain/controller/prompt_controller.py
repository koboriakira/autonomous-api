from abc import ABCMeta, abstractmethod
from app.common.dto.response import Response

class PromptController(metaclass=ABCMeta):
    @abstractmethod
    def handle(self) -> Response:
        pass

    async def handle_async(self) -> Response:
        pass
