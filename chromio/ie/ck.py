import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from aiofiles import open
from jsonschema import ValidationError as Error
from jsonschema import validate

# JSON Schema file path.
JSONSCHEMA_ASSET_PATH = "assets/schemas/exp-file.json"

# Validation error raised when schema not complied.
ValidationError = Error


@dataclass
class ExpFileChecker:
  """A component for the syntax check of an export file."""

  async def check(self, file_path: Path) -> None:
    """Verifies the syntax of a given file.

    Args:
      path: File path to check.

    Returns:
      True if the file is ok or a string with the syntax error message.

    Raises:
      FileNotFound: if file not found.
      ValidationError: if schema not complied.
    """

    # (1) read schema and content to validate
    schema = json.loads(resources.read_text("chromio", JSONSCHEMA_ASSET_PATH))

    async with open(file_path) as f:
      c = json.loads(await f.read())

    # (2) check the syntax
    validate(c, schema)
