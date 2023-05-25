from app.common.dto.response import Response
from app.prompt.domain.controller.prompt_controller import PromptController
from app.resolver.domain.controller.slack_controller import SlackController
import asyncio
from typing import Optional
from app.util.logger import get_logger
logger = get_logger(__name__)

class ApiV1():

    def __init__(self,
                 prompt_controller: PromptController,
                 slack_controller: Optional[SlackController]) -> None:
        self.prompt_controller = prompt_controller
        self.slack_controller = slack_controller

    def execute(self, user_content: Optional[dict]) -> Response:
        response = self.prompt_controller.handle(user_content=user_content)
        if response.is_ok():
            self.chat_postMessage(response.data["result"])
        return response

    async def execute_async(self, user_content: Optional[dict]) -> Response:
        logger.debug("execute_async")
        asyncio.create_task(self._execute_async(user_content=user_content))
        return Response(data="OK")

    async def _execute_async(self, user_content: Optional[dict]) -> Response:
        logger.debug("_execute_async")
        response = await self.prompt_controller.handle_async(user_content=user_content)
        logger.debug("_execute_async 2")
        if response.is_ok():
            logger.debug("chat_postMessage")
            self.chat_postMessage(response.data["result"])

    def chat_postMessage(self, text: str) -> None:
        if self.slack_controller is None:
            return
        if self.slack_controller.channel is None:
            return
        self.slack_controller.chat_postMessage(text)
