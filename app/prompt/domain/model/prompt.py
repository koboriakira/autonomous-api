from dataclasses import dataclass
from typing import Optional

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
    stop: str | None
    temperature: float
    timeout: int

    def __post_init__(self) -> None:
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")

    @staticmethod
    def of(messages: list,
           model: Optional[str] = None,
           max_tokens: Optional[int] = None,
           n: Optional[int] = None,
           stop: Optional[str] = None,
           temperature: Optional[float] = None,
           timeout: Optional[int] = None) -> 'Prompt':
        return Prompt(
            messages=messages,
            model=model if model is not None else INITIAL["model"],
            max_tokens=max_tokens if max_tokens is not None else INITIAL["max_tokens"],
            n=n if n is not None else INITIAL["n"],
            stop=stop if stop is not None else INITIAL["stop"],
            temperature=temperature if temperature is not None else INITIAL["temperature"],
            timeout=timeout if timeout is not None else INITIAL["timeout"],
        )
