from typing import Optional
from fastapi import FastAPI
import openai
import os
from openai_response_text import OpenaiResponseText
from openai.error import RateLimitError
from message_sample import get_message
from message_sample_second import get_message_second


openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
def read_root():
    try:
      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",      # モデル
          max_tokens=50,              # 生成する文章の最大単語数
          n=1,                        # いくつの返答を生成するか
          stop=None,                  # 指定した単語が出現した場合、文章生成を打ち切る
          temperature=0.8,            # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
          messages=get_message_second(),     # プロンプト
      )
      response_raw_text = response.choices[0].message.content
      response_text = OpenaiResponseText.from_raw_text(response_raw_text)
      return response_text.to_json()
    except RateLimitError as e:
      return {
        "result": None,
        "error": {
          "type": "RateLimitError",
          "message": str(e),
        }
      }
    except Exception as e:
      return {
        "result": None,
        "error": {
          "type": "UnknownError",
          "message": str(e),
        }
      }



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}