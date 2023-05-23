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
from common.dto.response import Response
from util.logger import get_logger
logger = get_logger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


class Counselling(BaseModel):
    text: str



app = FastAPI()



@app.get("/")
def read_root(query: Optional[str] = None):
    controller = PromptControllerImpl("healthcheck")
    return controller.handle()



@app.get("/sample_one/")
def read_item(query: Optional[str] = None):
    controller = PromptControllerImpl("sample_one")
    return controller.handle()


@app.post("/counselling/")
def counselling(counselling: Counselling):
    try:
        controller: PromptController = PromptControllerImpl(
            category="counselling",
            user_content=counselling.text)
        return controller.handle()
    except Exception as e:
        return {"error": str(e)}


class HowToCommand(BaseModel):
    command: str
    is_async: bool = False

@app.post("/how_to_command/")
async def how_to_command(how_to_command: HowToCommand):
    prompt_controller: PromptController = PromptControllerImpl(
        category="how_to_command",
        user_content=how_to_command.command)
    slack_controller = SlackControllerImpl(
        bot_user_oauth_token=os.getenv("BOT_USER_OAUTH_TOKEN"),
        channel="#openai")
    if how_to_command.is_async:
        asyncio.create_task(execute_how_to_command(
            prompt_controller, slack_controller))
        return {"data": "OK"}
    else:
        response = prompt_controller.handle()
        if response.is_ok():
            slack_controller.chat_postMessage(response.data["result"])
        return response


async def execute_how_to_command(prompt_controller: PromptController,
                                 slack_controller: SlackController) -> Response:
    try:
        response = await prompt_controller.handle_async()
        if response.is_ok():
            slack_controller.chat_postMessage(response.data["result"])
    except Exception as e:
        # TODO: ログを記録
        return {"error": str(e)}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
