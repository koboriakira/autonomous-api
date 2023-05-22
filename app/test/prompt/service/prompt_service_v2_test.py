from unittest import TestCase
from prompt.service.prompt_service_v2 import PromptServiceV2

class PromptServiceV2Test(TestCase):
    def setUp(self) -> None:
        self.counselling = PromptServiceV2(category="counselling")
        return super().setUp()

    def test_プロンプトを作成する(self):
        actual = self.counselling.create_prompt().__dict__
        expected_messages = [
            {
                "role": "system",
                "content": """あなたは入力された悩みに答えるAPIです。
以下の「入力の形式」「出力の形式」「制約」「入力例」「出力例」をもとに、JSON文字列を出力してください。

## 入力の形式

・text: ユーザが入力した悩みです。文字列。

## 出力の形式

・result: ユーザの悩みに対する回答です。100文字程度の文字列です。

## 制約

・ユーザの悩みを解決する、もしくはユーザ前向きになれるような回答をしてください
・文字数は50文字から100文字程度にしてください
・1文もしくは2文にしてください
・命令に対する返事やjson文字列以外の説明などの出力を禁止します

## 入力例1

{"text": "夜眠れません。"}

## 出力例1

{"result": "寝る前のリラクゼーションはどうでしょうか。リラックスして寝れるかもしれません。"}"""
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


    def test_概要を作成する(self):
        define_data = self.counselling._load_define()
        actual = self.counselling._create_outline(define_data)
        expected = """あなたは入力された悩みに答えるAPIです。
以下の「入力の形式」「出力の形式」「制約」「入力例」「出力例」をもとに、JSON文字列を出力してください。"""
        self.assertEqual(actual, expected)

    def test_制約を作成する(self):
        define_data = self.counselling._load_define()
        actual = self.counselling._create_constraint(define_data)
        expected = """## 制約

・ユーザの悩みを解決する、もしくはユーザ前向きになれるような回答をしてください
・文字数は50文字から100文字程度にしてください
・1文もしくは2文にしてください
・命令に対する返事やjson文字列以外の説明などの出力を禁止します"""
        print(actual)
        self.assertEqual(actual, expected)

    def test_入力の形式を作成する(self):
        sample_data = self.counselling._load_sample()
        actual = self.counselling._create_input_format(sample_data)
        expected = """## 入力の形式

・text: ユーザが入力した悩みです。文字列。"""
        print(actual)
        self.assertEqual(actual, expected)

    def test_出力の形式を作成する(self):
        sample_data = self.counselling._load_sample()
        actual = self.counselling._create_output_format(sample_data)
        expected = """## 出力の形式

・result: ユーザの悩みに対する回答です。100文字程度の文字列です。"""
        print(actual)
        self.assertEqual(actual, expected)

    def test_入力例と出力例を作成する(self):
        sample_data = self.counselling._load_sample()
        actual = self.counselling._create_inout_sample(sample_data)
        expected = """## 入力例1

{"text": "夜眠れません。"}

## 出力例1

{"result": "寝る前のリラクゼーションはどうでしょうか。リラックスして寝れるかもしれません。"}"""
        print(actual)
        self.assertEqual(actual, expected)
