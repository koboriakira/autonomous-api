from dataclasses import dataclass
import json
import re

@dataclass(frozen=True)
class OpenaiResponseText:
    value: str

    @staticmethod
    def from_raw_text(raw_text: str) -> "OpenaiResponseText":
        return OpenaiResponseText(raw_text.replace("\n", ""))

    def to_json(self) -> dict | list:
        try:
            json_data = json.loads(self.value)
            return json_data
        except:
            print(self.value)
            print("\n\n\n")
            pattern = r".*```json"
            replaced_str = re.sub(pattern, "", self.value)
            print(replaced_str)
            print("\n\n\n")
            pattern = r"```.*"
            replaced_str = re.sub(pattern, "", replaced_str)
            try:
                json_data = json.loads(replaced_str)
                return json_data
            except:
                return {
                    "result": "JSONデータへのエンコードに失敗しました。",
                    "text": replaced_str,
                    "originalText": self.value,
                }

if __name__ == '__main__':
    suite2 = OpenaiResponseText.from_raw_text(
        "以下のように、ジョーク本文をresultキーに格納したJSON文字列を出力します。\n\n```json\n{\n    \"result\": \"Why do programmers prefer dark mode? Because light attracts bugs.\"\n}\n```")
    print(suite2.to_json())
