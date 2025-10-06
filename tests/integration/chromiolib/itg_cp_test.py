import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection

from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from chromio.ie.cp import CollCopier


@pytest.fixture(scope="module")
def copier() -> CollCopier:
  """Copier to use in the tests."""

  return CollCopier(batch_size=DEFAULT_BATCH_SIZE, fields=DEFAULT_FIELDS)


@pytest.mark.attr(id="ITG-CP-01")
@pytest.mark.usefixtures("arrange_coll")
async def test_export_coll_fully(
  copier: CollCopier, src_coll: AsyncCollection, dst_coll: AsyncCollection
) -> None:
  """Check that CollCopier.copy_coll() performs this expected."""

  # (1) precondition: collection has greater than two records
  assert (count := await src_coll.count()) > 2

  # (2) act
  out = await copier.copy_coll(src_coll, dst_coll)

  # (3) assessment
  # report
  assert out.coll == src_coll.name
  assert out.dst_coll == dst_coll.name
  assert out.count == count

  # db state
  assert count == await dst_coll.count()


@pytest.mark.attr(id="ITG-CP-02")
@pytest.mark.usefixtures("arrange_coll")
async def test_export_coll_partially(
  copier: CollCopier, src_coll: AsyncCollection, dst_coll: AsyncCollection
) -> None:
  """Check that CollCopier.copy_coll() performs this expected when limit set."""

  limit = 2

  # (1) precondition: collection has greater than two records
  assert await src_coll.count() > limit

  # (2) act
  out = await copier.copy_coll(src_coll, dst_coll, limit=limit)

  # (3) assessment
  # report
  assert out.coll == src_coll.name
  assert out.dst_coll == dst_coll.name
  assert out.count == limit

  # db state
  assert await dst_coll.count() == limit
