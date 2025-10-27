from pathlib import Path

import pytest
from chromadb.api import AsyncClientAPI
from pytest import CaptureFixture, Pytester


@pytest.mark.attr(id="E2E-02")
async def test_dl_imp_flow(
  pytester: Pytester,
  tmp_path: Path,
  capsys: CaptureFixture,
  db: AsyncClientAPI,
) -> None:
  """Check that the flow download-import works ok."""

  # (1) arrange
  exp_file = tmp_path / "dl.json"

  # (2) act
  dl_out = pytester.run("chromie", "dl", "-c", "tests", exp_file)
  imp_out = pytester.run("chromie", "imp", exp_file, "server://///dl_imp")
  capsys.readouterr()

  # (3) assessment
  # terminal
  assert dl_out.ret == 0
  assert imp_out.ret == 0

  dl_out.stdout.re_match_lines_random((r"Downloading", r"Checking"))
  imp_out.stdout.re_match_lines_random(
    (
      r"Collection: dl_imp",
      r"Count: 10",
      r"Duration \(s\): .+",
    ),
  )

  # imported collection
  coll = await db.get_collection("dl_imp")
  assert await coll.count() == 10

  # (4) clean up
  await db.delete_collection("dl_imp")
