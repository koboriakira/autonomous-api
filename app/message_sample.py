def get_message():
    return [
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
    ]
