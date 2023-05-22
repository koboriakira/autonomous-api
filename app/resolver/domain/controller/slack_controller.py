from abc import ABCMeta, abstractmethod


class SlackController(metaclass=ABCMeta):
    @abstractmethod
    def chat_postMessage(self, text: str) -> bool:
        pass
