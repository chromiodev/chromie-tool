from pathlib import Path

import pytest
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import CaptureFixture, Pytester


@pytest.mark.attr(id="E2E-01")
@pytest.mark.usefixtures("arrange_coll")
async def test_exp_imp_flow(
  pytester: Pytester,
  tmp_path: Path,
  capsys: CaptureFixture,
  db: AsyncClientAPI,
  coll: AsyncCollection,
) -> None:
  """Check that the flow export-import works ok."""

  # (1) precondition
  assert (count := await coll.count()) > 1

  # (2) arrange
  exp_file = tmp_path / "export.json"

  # (3) act
  exp_out = pytester.run("chromie", "exp", "server://///pytest", exp_file)
  imp_out = pytester.run("chromie", "imp", exp_file, "server://///exp_imp")
  capsys.readouterr()

  # (4) assessment
  # terminal
  assert exp_out.ret == 0
  assert imp_out.ret == 0

  exp_out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      rf"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  imp_out.stdout.re_match_lines_random(
    (
      r"Collection: exp_imp",
      rf"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # imported collection
  coll = await db.get_collection("exp_imp")
  assert await coll.count() == count

  # (5) clean up
  await db.delete_collection("exp_imp")
