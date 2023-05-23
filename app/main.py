from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import openai
import os
import asyncio
from prompt.domain.controller.prompt_controller import PromptController
from prompt.controller.prompt_controller_impl import PromptControllerImpl
from resolver.domain.controller.slack_controller import SlackController
from resolver.controller.slack_controller_impl import SlackControllerImpl
from api.v1.api import ApiV1
from util.logger import get_logger
logger = get_logger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


class CommandRequest(BaseModel):
    request: dict



app = FastAPI()



@app.get("/")
def read_root(query: Optional[str] = None):
    controller = PromptControllerImpl("healthcheck")
    return controller.handle()


@app.post("/{category}/")
async def command(category: str, commandRequest: CommandRequest):
    logger.info(f'command: %s' % category)
    request = commandRequest.request
    user_content = request["user_content"]
    controller: PromptController = PromptControllerImpl(
        category=category,
        user_content=user_content)
    # slack_controller = SlackControllerImpl(
    #     bot_user_oauth_token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"),
    #     channel_id=request["channel"],
    # )
    slack_controller = None
    api = ApiV1(
        prompt_controller=controller,
        slack_controller=slack_controller)
    return await api.execute(request)



# @app.post("/{command}/")
# async def how_to_command(command: str, request: HowToCommandRequest):
#     api = HowToCommandApi(request)
#     return await api.execute(request)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
