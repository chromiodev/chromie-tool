from pathlib import Path

import pytest
from pytest import CaptureFixture, Pytester


@pytest.mark.attr(id="FN-CK-01")
async def test_check_valid_file(
  pytester: Pytester,
  capsys: CaptureFixture,
  data_dir: Path,
) -> None:
  """Check that 'chromie check' exits with 0 when OK."""

  # (1) precondition/arrange
  file_path = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (2) act
  out = pytester.run("chromie", "check", file_path)
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random("OK")


@pytest.mark.attr(id="FN-CK-02")
async def test_check_invalid_file(pytester: Pytester, capsys: CaptureFixture) -> None:
  """Check that 'chromie check' exits with 0 when OK."""

  # (1) precondition/arrange
  file_path = pytester.makefile(
    ".json",
    exp="""
    {
      "version": "1.0",
      "metadata": {
        "chroma": {"version": "1.1.0"},
        "coll": {"name": "test"}
      },
      "data": {}
    }
  """,
  )

  # (2) act
  out = pytester.run("chromie", "check", file_path)
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 1
  out.stderr.re_match_lines_random(".*is not of type 'array'.*")
