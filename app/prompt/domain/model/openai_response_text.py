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
            pattern = r".*```json"
            replaced_str = re.sub(pattern, "", self.value)
            pattern = r"```.*"
            replaced_str = re.sub(pattern, "", replaced_str)
            try:
                json_data = json.loads(replaced_str)
                return json_data
            except:
                raise Exception({
                    "result": "JSONデータへのエンコードに失敗しました。",
                    "text": replaced_str,
                    "originalText": self.value,
                })
