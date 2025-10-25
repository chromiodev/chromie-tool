from pathlib import Path

import pytest
from aiofiles import open

from chromio.ie.ck import ExpFileChecker, ValidationError


@pytest.fixture
def checker() -> ExpFileChecker:
  """Checker to use in the tests."""

  return ExpFileChecker()


async def test_check_file_is_ok(data_dir: Path, checker: ExpFileChecker) -> None:
  """Check that the check() method returning None if an export file is ok."""

  # (1) act
  out = await checker.check(data_dir / "cc-export.json")

  # (2) assessment
  assert out is None


async def test_check_raises_validation_error(
  tmp_path: Path, checker: ExpFileChecker
) -> None:
  """Check that the check() method raises ValidationError when an error detected."""

  # (1) arrange
  file_path = tmp_path / "cc-export.json"

  async with open(file_path, "w") as f:
    await f.write("""
      {
        "version": "1.0",
        "metadata": {
          "chroma": {"version": "1.1.0"},
          "coll": {"name": "test"}
        },
        "data": {
        }
      }
    """)

  # (2) act and assessment
  with pytest.raises(ValidationError, match="is not of type 'array'"):
    await checker.check(file_path)


async def test_check_raises_file_not_found_error(
  tmp_path: Path, checker: ExpFileChecker
) -> None:
  """Check that the check() method raises FileNotFoundError when an error detected."""

  with pytest.raises(
    FileNotFoundError, match="No such file or directory: 'unknown.json'"
  ):
    await checker.check(Path("unknown.json"))
