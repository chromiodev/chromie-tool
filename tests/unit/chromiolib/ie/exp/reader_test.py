import pytest
from pytest import FixtureRequest
from pytest_mock import AsyncMockType

from chromio.ie import Field
from chromio.ie.exp.reader import CollReader


@pytest.fixture(scope="module")
def reader() -> CollReader:
  """Collection reader to use in the tests."""

  return CollReader()


@pytest.fixture(scope="function")
def results(request: FixtureRequest) -> list[dict]:
  """Indirect fixture for getting the GetResult to use in the tests."""

  one = {
    "ids": ["1", "2"],
    "metadatas": [{"x": 11}, {"x": 22}],
    "documents": ["one", "two"],
  }

  two = {
    "ids": ["3", "4"],
    "metadatas": [{"x": 33}, {"x": 44}],
    "documents": ["three", "four"],
  }

  three = {
    "ids": ["5"],
    "metadatas": [{"x": 55}],
    "documents": ["five"],
  }

  match id := request.param:
    case "one":
      return [one]

    case "two":
      return [one, two]

    case "three":
      return [one, two, three]

    case _:
      raise ValueError(f"Unexpected indirect fixture value: {id}")


@pytest.mark.parametrize(
  ("limit", "batches", "results"),
  (
    pytest.param(2, [2], "one", id="2"),
    pytest.param(4, [2, 2], "two", id="2, 2"),
    pytest.param(5, [2, 2, 1], "three", id="2, 2, 1"),
  ),
  indirect=["results"],
)
async def test_read_coll(
  coll: AsyncMockType,
  reader: CollReader,
  limit: int,
  batches: list[int],
  results: dict,
) -> None:
  """Check that read() returns a given number of batches with its correct sizes."""

  # (1) arrange
  fields = [Field.id, Field.meta, Field.doc]
  (get := coll.get).side_effect = results

  # (2) act
  out = [batch async for batch in reader.read(coll, fields, batch_size=2, limit=limit)]

  # (3) assessment
  assert get.await_count == len(batches)
  assert len(out) == len(batches)

  for i in range(len(batches)):
    assert len(batch := out[i]) == batches[i]

    for rec in batch:
      assert "id" in rec
      assert "metadata" in rec
      assert "document" in rec
      assert "embedding" not in rec


async def test_read_empty_coll(coll: AsyncMockType, reader: CollReader) -> None:
  """Check that read() returns nothing if empty collection."""

  # (1) arrange
  fields = [Field.id, Field.meta, Field.doc]
  (get := coll.get).return_value = {"ids": [], "metadatas": [], "documents": []}

  # (2) act
  out = [batch async for batch in reader.read(coll, fields, batch_size=2, limit=10)]

  # (3) assessment
  assert get.await_count == 1
  assert out == []


async def test_read_only_id(coll: AsyncMockType, reader: CollReader) -> None:
  """Check that read() only returns id when fields == [Field.id]."""

  # (1) arrange
  fields = [Field.id]
  (get := coll.get).side_effect = [
    {"ids": ["1", "2"], "metadatas": None, "documents": None},
    {"ids": [], "metadatas": None, "documents": None},
  ]

  # (2) act
  out = [batch async for batch in reader.read(coll, fields, batch_size=2, limit=10)]

  # (3) assessment
  assert get.await_count == 2
  assert len(out) == 1

  for i in range(1):
    for rec in out[0]:
      assert "id" in rec
      assert "metadata" not in rec
      assert "document" not in rec
      assert "embedding" not in rec
