import json

import pytest
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import CaptureFixture, Pytester

# Implicit pytest marks.
pytestmark = [pytest.mark.usefixtures("arrange_coll")]


@pytest.mark.readonly
@pytest.mark.attr(id="FN-EXP-01")
async def test_export_existing_coll(
  pytester: Pytester, capsys: CaptureFixture, coll: AsyncCollection
) -> None:
  """Check that 'chromie exp' exports an existing collection."""

  # (1) precondition
  assert (count := await coll.count()) > 1

  # (2) arrange
  outfile = pytester.makefile(".json", export="")

  # (3) act
  out = pytester.run("chromie", "exp", "server://///pytest", outfile)
  capsys.readouterr()

  # (4) assessment
  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      f"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # valid json
  assert isinstance(out := json.loads(outfile.read_text()), dict)

  # file content
  assert out["version"] == "1.0"
  assert out["metadata"] == {"chroma": {"version": "1.0.0"}, "coll": {"name": "pytest"}}
  assert len(out["data"]) == count


@pytest.mark.readonly
@pytest.mark.attr(id="FN-EXP-03")
async def test_export_unknown_coll(
  pytester: Pytester, capsys: CaptureFixture, db: AsyncClientAPI
) -> None:
  """Check that 'chromie exp' returns error if the collection is unknown."""

  coll_name = "unknown"

  # (1) precondition: collection does not exist
  try:
    await db.delete_collection(coll_name)
  except Exception:
    pass

  # (2) act
  out = pytester.run("chromie", "exp", f"server://///{coll_name}", "export.json")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 1
  out.stderr.re_match_lines_random((r"Collection .unknown. does not exist",))
