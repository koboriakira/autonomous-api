from abc import ABCMeta, abstractmethod
from domain.interface.gateway.dto.response import Response


class Controller(metaclass=ABCMeta):
    @abstractmethod
    def handle(self) -> Response:
        pass
