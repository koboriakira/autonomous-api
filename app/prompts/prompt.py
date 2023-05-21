from dataclasses import dataclass
from typing import Any
import yaml
import os

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


    @staticmethod
    def get_chat_completion_args() -> 'Prompt':
        with open(DIR_NAME + '/sample_one/define.yaml') as file:
            obj = yaml.safe_load(file)
            system_message: str = obj["prompt"]["system"]
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
