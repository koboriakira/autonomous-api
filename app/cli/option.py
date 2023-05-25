from dataclasses import dataclass
from argparse import Namespace


@dataclass(frozen=True)
class Option:
    command: str = None

    @staticmethod
    def from_args(args: Namespace) -> 'Option':
        return Option(
            command=args.command,
        )

    def to_user_content(self) -> dict:
        result = {}
        if self.command is not None:
            result["command"] = self.command
        return result
