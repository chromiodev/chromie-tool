import pytest
from pytest import FixtureRequest
from pytest_mock import AsyncMockType

from chromio.ie import Field
from chromio.ie.imp.writer import CollWriter


@pytest.fixture(scope="module")
def writer() -> CollWriter:
  """Writer to use in the tests."""

  return CollWriter()


@pytest.fixture(scope="function")
def records(request: FixtureRequest, qt_records: list[dict]) -> list[dict]:
  """Records to use in the tests."""

  return [r | {"embedding": [0.1, 0.2]} for r in qt_records[0 : request.param]]


@pytest.mark.parametrize(
  ("records", "batch_size", "limit", "e", "e_batches"),
  (
    pytest.param(5, 2, 3, 3, 2),
    pytest.param(5, 2, None, 5, 3),
    pytest.param(2, 2, 5, 2, 1),
  ),
  indirect=("records",),
)
async def test_write_records_with_default_fields(
  writer: CollWriter,
  coll: AsyncMockType,
  records: list[dict],
  batch_size: int,
  limit: int | None,
  e: int,
  e_batches: int,
) -> None:
  """Check that write() writes records (w/o fields set) correctly in the collection."""

  # (1) arrange
  (add := coll.add).return_value = None

  # (2) act
  out = await writer.write(records, coll, batch_size=batch_size, limit=limit)

  # (3) assessment
  assert out == e
  assert add.await_count == e_batches

  for call in add.await_args_list:
    assert call.kwargs["metadatas"] is not None
    assert call.kwargs["embeddings"] is None


@pytest.mark.parametrize(
  ("records", "batch_size", "limit", "e", "e_batches"),
  (
    pytest.param(5, 2, 3, 3, 2),
    pytest.param(5, 2, None, 5, 3),
    pytest.param(2, 2, 5, 2, 1),
  ),
  indirect=("records",),
)
async def test_write_records_with_embedding(
  writer: CollWriter,
  coll: AsyncMockType,
  records: list[dict],
  batch_size: int,
  limit: int | None,
  e: int,
  e_batches: int,
) -> None:
  """Check that write() writes records (w/ fields set) correctly in the collection."""

  # (1) arrange
  fields = [Field.meta, Field.embedding]
  (add := coll.add).return_value = None

  # (2) act
  out = await writer.write(
    records, coll, fields=fields, batch_size=batch_size, limit=limit
  )

  # (3) assessment
  assert out == e
  assert add.await_count == e_batches

  for call in add.await_args_list:
    assert call.kwargs["metadatas"] is not None
    assert call.kwargs["embeddings"] is not None
