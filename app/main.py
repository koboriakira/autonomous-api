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

class SlackRequest(BaseModel):
    token: str
    channel: str

class CommandRequest(BaseModel):
    version: int = Field(..., example=1)
    user_content: Optional[dict] = Field(None, example={"text": "hello"})
    is_async: Optional[bool] = Field(False, example=True)
    slack: Optional[SlackRequest] = Field(None,
                                          example={"token": "xoxb-xxxx",
                                                   "channel": "#channel"})


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
        bot_user_oauth_token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"),
        channel="#openai")
    if not os.getenv("IS_DEV"):
        slack_controller = None
    api = ApiV1(
        prompt_controller=controller,
        slack_controller=slack_controller)
    return await _execute_api_v1(api, request)


@app.post("/{category}/")
async def command(category: str, request: CommandRequest):
    match request.version:
        case 1:
            logger.info(f'command: %s' % category)
            controller: PromptController = PromptControllerImpl(
                category=category)
            slack_controller = _get_slack_controller(request.slack)
            logger.debug(f'slack_controller: %s' % slack_controller)
            api = ApiV1(
                prompt_controller=controller,
                slack_controller=slack_controller)
            return await _execute_api_v1(api, request)
        case _:
            return {"error": "invalid version"}


async def _execute_api_v1(api: ApiV1, request: CommandRequest):
    if request.is_async:
        return await api.execute_async(user_content=request.user_content)
    else:
        return api.execute(user_content=request.user_content)


def _get_slack_controller(request: dict) -> Optional[SlackController]:
    if "slack" in request:
        slack_request = request["slack"]
        if "token" in slack_request and "channel" in slack_request:
            return SlackControllerImpl(
                bot_user_oauth_token=slack_request["token"],
                channel=slack_request["channel"])
    return None
