import pytest
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import CaptureFixture, Pytester

# Implicit pytest marks.
pytestmark = [pytest.mark.usefixtures("arrange_coll")]


@pytest.mark.attr(id="FN-CP-01")
@pytest.mark.usefixtures("arrange_coll")
async def test_copy_existing_coll(
  pytester: Pytester,
  capsys: CaptureFixture,
  src_coll: AsyncCollection,
  dst_coll: AsyncCollection,
) -> None:
  """Check that 'chromie cp' copies an existing collection."""

  # (1) precondition
  assert (count := await src_coll.count()) > 1

  # (2) act
  out = pytester.run(
    "chromie", "cp", f"server://///{src_coll.name}", f"server://///{dst_coll.name}"
  )

  capsys.readouterr()

  # (3) assessment
  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      f"Source collection: {src_coll.name}",
      f"Destination collection: {dst_coll.name}",
      f"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # destination collection
  assert await dst_coll.count() == count


@pytest.mark.attr(id="FN-CP-02")
async def test_copy_unreachable_coll(
  pytester: Pytester, capsys: CaptureFixture, db: AsyncClientAPI
) -> None:
  """Check that 'chromie cp' returns error if the source collection is unreachable."""

  src_coll_name = "unknown_source"

  # (1) precondition: collection does not exist
  try:
    await db.delete_collection(src_coll_name)
  except Exception:
    pass

  # (2) act
  out = pytester.run(
    "chromie", "cp", f"server://///{src_coll_name}", "server://///any_dest"
  )

  capsys.readouterr()

  # (3) assessment
  assert out.ret != 0
  out.stderr.re_match_lines_random((rf"Collection .{src_coll_name}. does not exist",))
