from typing import Optional
from fastapi import FastAPI
import openai
import os
from openai_response_text import OpenaiResponseText
from openai.error import RateLimitError

openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
def read_root():
    try:
      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",      # モデル
          max_tokens=50,             # 生成する文章の最大単語数
          n=1,                        # いくつの返答を生成するか
          stop=None,                  # 指定した単語が出現した場合、文章生成を打ち切る
          temperature=0.8,            # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
          messages=[
              {
                  "role": "system",
                  "content": """
  あなたはAPIサーバの内部処理です。
  あなたが返答した出力はJSONのデータとして利用されるため、出力はかならずJSON文字列のみにしてください。
  JSON文字列とならない出力は禁止します。
  """
              },
              {
                  "role": "system",
                  "content": """
  出力してほしいJSON文字列の形式は次のとおりです。

  ```json
  {
      "result": "ここにあなたの返答を入れる"
  }
  ```

  resultキーに対応する値に、あなたの返答を入れてください。
  """
              },
              {
                  "role": "user",
                  "content": """
  以下の制約をもとに、。

  ## 制約

  ・次のようにJSON文字列になるように出力してください。

  ```json
  {
      "result": "ここにあなたの返答を入れる"
  }
  ```

  ・ジョーク本文のみをJSON形式のresultキーに格納する

  ## OK例

  下記の出力は、JSON文字列になっています。
  応答やPythonのコードなど不要な文章はひとつも出力されていません。

  \"\"\"
  {\n    \"result\": \"Why do programmers prefer dark mode? Because light attracts bugs.\"\n}
  \"\"\"

  ## NG例

  次の出力は、JSON文字列になっていません。

  \"\"\"
  了解しました。以下のジョークを出力します。\n\n```json\n{\n    \"result\": \"Why do programmers prefer dark mode? Because light attracts bugs.\"\n}\n```
  \"\"\"

  """
              }
          ],
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
