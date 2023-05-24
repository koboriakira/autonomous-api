from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import openai
import os
from app.prompt.domain.controller.prompt_controller import PromptController
from app.prompt.controller.prompt_controller_impl import PromptControllerImpl
from app.resolver.domain.controller.slack_controller import SlackController
from app.resolver.controller.slack_controller_impl import SlackControllerImpl
from app.api.v1.api import ApiV1
from app.util.logger import get_logger
logger = get_logger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


class CommandRequest(BaseModel):
    request: dict


app = FastAPI()


@app.get("/")
async def read_root():
    request = {
        "slack": {
            "channel": "#openai"
        }
    }
    logger.info("healthcheck!!!")
    controller = PromptControllerImpl(category="healthcheck")
    slack_controller = SlackControllerImpl(
        bot_user_oauth_token=os.getenv("BOT_USER_OAUTH_TOKEN"),
        channel=request["slack"]["channel"] if "slack" in request and "channel" in request["slack"] else None)
    api = ApiV1(
        prompt_controller=controller,
        slack_controller=slack_controller)
    return await api.execute()


@app.post("/{category}/")
async def command(category: str, commandRequest: CommandRequest):
    version:int = request["version"]
    match version:
        case 1:
            logger.info(f'command: %s' % category)
            request = commandRequest.request
            user_content = request["user_content"]
            controller: PromptController = PromptControllerImpl(
                category=category,
                user_content=user_content)
            slack_controller = SlackControllerImpl(
                bot_user_oauth_token=os.getenv("BOT_USER_OAUTH_TOKEN"),
                channel=request["slack"]["channel"] if "slack" in request and "channel" in request["slack"] else None)
            api = ApiV1(
                prompt_controller=controller,
                slack_controller=slack_controller)
            return await api.execute()
        case _:
            return {"error": "invalid version"}

def _is_async(self, request: dict) -> bool:
    return "is_async" in request and request["is_async"]
