from typing import Optional
from fastapi import FastAPI
import openai
import os
from domain.controller.controller import Controller
from controller.controller_impl import ControllerImpl

openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()



@app.get("/")
def read_root(query: Optional[str] = None):
    controller: Controller = ControllerImpl("sample_one")
    return controller.handle()


@app.get("/healthcheck/")
def read_item(query: Optional[str] = None):
    controller: Controller = ControllerImpl("healthcheck")
    return controller.healthcheck()


@app.get("/sample_one/")
def read_item(query: Optional[str] = None):
    controller: Controller = ControllerImpl("sample_one")
    return controller.handle()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
