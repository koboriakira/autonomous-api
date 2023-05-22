from dataclasses import dataclass
from typing import Any
import yaml
import os
import json

DIR_NAME = os.path.dirname(__file__)
INITIAL = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 150,
    "n": 1,
    "stop": None,
    "temperature": 1.3,
    "timeout": 60,
}

@dataclass(frozen=True)
class Prompt():
    messages: list
    model: str
    max_tokens: int
    n: int
    stop: str|None
    temperature: float
    timeout: int

    def __post_init__(self) -> None:
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")


    @classmethod
    def get_chat_completion_args(cls, category: str) -> 'Prompt':
        "${category}"
        with open(f'%s/%s/define.yaml' % (DIR_NAME, category)) as file:
            obj = yaml.safe_load(file)
            system_message: str = obj["prompt"]["system"] + \
                "\n\n" + cls._get_inout_example(category)
            return Prompt(
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    }
                ],
                model=obj["model"] if "model" in obj else INITIAL["model"],
                max_tokens=obj["max_tokens"] if "max_tokens" in obj else INITIAL["max_tokens"],
                n=obj["n"] if "n" in obj else INITIAL["n"],
                stop=obj["stop"] if "stop" in obj else INITIAL["stop"],
                temperature=obj["temperature"] if "temperature" in obj else INITIAL["temperature"],
                timeout=obj["timeout"] if "timeout" in obj else INITIAL["timeout"],
            )

    @classmethod
    def _get_inout_example(cls, category: str) -> str:
        with open(f'%s/%s/sample.yaml' % (DIR_NAME, category)) as file:
            obj: list[dict] = yaml.safe_load(file)
            result = ""
            for idx, item in enumerate(obj):
                if "input" in item:
                    pass
                if "output" in item:
                    result += f"\n## 出力例{idx+1}\n\n"
                    result += json.dumps(item["output"], ensure_ascii=False)
                    result += "\n"
            result = result.strip()
            return result

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "n": self.n,
            "stop": self.stop,
            "temperature": self.temperature,
            "timeout": self.timeout,
            "messages": self.messages,
        }
