from typing import Optional
from fastapi import FastAPI
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
def read_root():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",      # モデル
        messages=[
            {
                "role": "system",
                "content": """
あなたはAPIです。
Pythonを使ってあなたが返答した出力をJSONデータに変換するため、出力はかならずJSON形式にしてください。
"""
            },
            {
                "role": "system",
                "content": """
以下のJSONの形式になるように出力をしてください。

```json
{
    "result": "ここにあなたの返答を入れる"
}
```
"""
            },
            {
                "role": "system",
                "content": """
JSONデータへのエンコードが失敗してしまうような、関係ない出力を禁止します。
出力前後の挨拶や、"```"を使ったコードブロックに入れることも禁止します。
"""
            },
            {
                "role": "user",
                "content": """
以下の制約をもとに、ジョークを出力してください。

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
        max_tokens=100,             # 生成する文章の最大単語数
        n=1,                        # いくつの返答を生成するか
        stop=None,                  # 指定した単語が出現した場合、文章生成を打ち切る
        temperature=1.5,            # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )
    response_raw_text = response.choices[0].message.content
    try:
        json_data = json.loads(response_raw_text)
        return json_data
    except:
        return {
            "result": "JSONデータへのエンコードに失敗しました。",
            "text": response_raw_text
        }



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
