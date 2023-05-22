from abc import ABCMeta, abstractmethod
from common.dto.response import Response

class PromptController(metaclass=ABCMeta):
    @abstractmethod
    def handle(self) -> Response:
        pass
