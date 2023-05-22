from unittest import TestCase
from prompt.service.prompt_service_v1 import PromptServiceV1

class PromptServiceV1Test(TestCase):
    def setUp(self) -> None:
        self.sample_one = PromptServiceV1(category="sample_one")
        return super().setUp()

    def test_define_yamlを変換する(self):
        actual = self.sample_one.create_prompt().__dict__
        expected_messages = [
            {
                "role": "system",
                "content": """あなたは朝の挨拶を出力するAPIです。
以下の「レスポンスの形式」と「制約」をもとに、JSON文字列を出力してください。

## レスポンスの形式

{
  "result": "今日も開発をがんばりましょう！"
}

・result: 朝の挨拶のメッセージを出力してください。文字列

## 制約

・メッセージを受けとる人物の職業はエンジニアなので、エンジニアやITに関連するキーワードが盛り込まれていると素晴らしいです
・出力されたメッセージを受けとった側がポジティブな気持ちになれるようなメッセージにしてください
・命令に対する返事やjson文字列以外の説明などの出力を禁止します
・文字数は50文字から100文字程度にしてください。
・1文もしくは2文にしてください。

## 出力例1

{"result": "今日も開発をがんばりましょう！"}

## 出力例2

{"result": "素晴らしいプロダクトが開発できますように！"}

## 出力例3

{"result": "あなたなら難しい設計もできるはずです！"}"""
            }
        ]
        expected = {
            "model": "gpt-3.5-turbo",
            "max_tokens": 150,
            "n": 1,
            "stop": None,
            "temperature": 1.3,
            "timeout": 20,
            "messages": expected_messages,
        }
        self.assertEqual(actual["model"], expected["model"])
        self.assertEqual(actual["max_tokens"], expected["max_tokens"])
        self.assertEqual(actual["n"], expected["n"])
        self.assertEqual(actual["stop"], expected["stop"])
        self.assertEqual(actual["temperature"], expected["temperature"])
        self.assertEqual(actual["timeout"], expected["timeout"])
        self.assertEqual(actual["messages"], expected["messages"])