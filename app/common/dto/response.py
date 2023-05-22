
from dataclasses import dataclass
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class ErrorType(Enum):
    RATE_LIMIT_ERROR = 'RateLimitError'
    UNKNOWN_ERROR = 'UnknownError'


@dataclass
class Error:
    type: ErrorType
    message: str


@dataclass
class Response:
    data: Any = None
    error: Optional[Error] = None
    raw_data: Optional[str] = None

    def is_ok(self)-> bool:
        return self.data is not None and self.error is None
