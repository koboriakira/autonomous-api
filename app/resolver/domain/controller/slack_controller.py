from abc import ABCMeta, abstractmethod
from slack_sdk.web.client import WebClient


class SlackController(metaclass=ABCMeta):
    channel: str
    slackbot: WebClient

    @abstractmethod
    def chat_postMessage(self, text: str) -> bool:
        pass
