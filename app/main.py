from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import openai
import os
from prompt.domain.controller.prompt_controller import PromptController
from prompt.controller.prompt_controller_impl import PromptControllerImpl
openai.api_key = os.getenv("OPENAI_API_KEY")


class Counselling(BaseModel):
    text: str



app = FastAPI()



@app.get("/")
def read_root(query: Optional[str] = None):
    controller: PromptController = PromptControllerImpl(
        "healthcheck")
    return controller.handle()



@app.get("/sample_one/")
def read_item(query: Optional[str] = None):
    controller: PromptController = PromptControllerImpl("sample_one")
    return controller.handle()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/counselling/")
def counselling(counselling: Counselling):
    try:
        user_content = counselling.text
        print(user_content)
        controller: PromptController = PromptControllerImpl(
            category="counselling",
            user_content=user_content)
        return controller.handle()
    except Exception as e:
        return {"error": str(e)}


class HowToCommand(BaseModel):
    command: str

@app.post("/how_to_command/")
def how_to_command(how_to_command: HowToCommand):
    try:
        controller: PromptController = PromptControllerImpl(
            category="how_to_command",
            user_content=how_to_command.command)
        return controller.handle()
    except Exception as e:
        return {"error": str(e)}
