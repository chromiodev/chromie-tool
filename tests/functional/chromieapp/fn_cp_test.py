from typing import AsyncIterator

import pytest
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import CaptureFixture, Pytester

# Implicit pytest marks.
pytestmark = [pytest.mark.usefixtures("arrange_coll")]


@pytest.fixture(scope="function")
async def dst_coll(db: AsyncClientAPI) -> AsyncIterator[AsyncCollection]:
  """Collection to use in the tests as destination."""

  # (1) truncate collection
  coll = await db.create_collection("pytest_cp", get_or_create=True)
  await coll.delete(where={"id": {"$ne": "unknown"}})

  # (2) return collection
  yield coll

  # (3) drop collection
  await db.delete_collection(coll.name)


@pytest.mark.attr(id="FN-CP-01")
@pytest.mark.usefixtures("arrange_coll")
async def test_copy_existing_coll(
  pytester: Pytester,
  capsys: CaptureFixture,
  coll: AsyncCollection,
  dst_coll: AsyncCollection,
) -> None:
  """Check that 'chromie cp' copies an existing collection."""

  # (1) precondition
  print(coll.name)
  assert (count := await coll.count()) > 1

  # (2) act
  out = pytester.run(
    "chromie", "cp", f"server://///{coll.name}", f"server://///{dst_coll.name}"
  )

  capsys.readouterr()

  # (3) assessment
  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      f"Source collection: {coll.name}",
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
