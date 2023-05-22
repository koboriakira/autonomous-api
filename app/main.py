from typing import Optional
from fastapi import FastAPI
import openai
import os
from prompt.domain.controller.prompt_controller import PromptController
from prompt.controller.prompt_controller_impl import PromptControllerImpl
openai.api_key = os.getenv("OPENAI_API_KEY")


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
