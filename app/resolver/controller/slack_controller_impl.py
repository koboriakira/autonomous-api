from slack_sdk.web.client import WebClient
from app.resolver.domain.controller.slack_controller import SlackController
from app.util.logger import get_logger
logger = get_logger(__name__)

class SlackControllerImpl(SlackController):

    def __init__(self, bot_user_oauth_token: str, channel: str) -> None:
        self.slackbot = WebClient(token=bot_user_oauth_token)
        self.channel = channel

    def chat_postMessage(self, text: str) -> bool:
        logger.info(f"SlackControllerImpl.chat_postMessage: {text}")
        self.slackbot.chat_postMessage(
            channel=self.channel,
            text=text)
