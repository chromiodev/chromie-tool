import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.ie.ck import ExpFileChecker, ValidationError
from chromio.tools import Cmd


@dataclass(frozen=True)
class CheckCmd(Cmd):
  # @override
  name: str = "check"

  # @override
  help: str = "Validate an export file with the export schema."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["src"],
        "help": "file path to validate",
        "required": True,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    try:
      checker = ExpFileChecker()
      await checker.check(args.src)
      print("OK")
    except ValidationError as e:
      print(e, file=sys.stderr)
      exit(1)
    except FileNotFoundError as e:
      print(e, file=sys.stderr)
      exit(1)
