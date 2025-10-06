from math import ceil

import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest_mock import AsyncMockType, MockerFixture

from chromio.ie.consts import DEFAULT_FIELDS
from chromio.ie.cp import CollCopier


@pytest.fixture(scope="module")
def copier(default_batch_size: int) -> CollCopier:
  """Exporter to use in the tests."""

  return CollCopier(batch_size=default_batch_size, fields=DEFAULT_FIELDS)


@pytest.fixture(scope="function")
def dst_coll(mocker: MockerFixture) -> AsyncMockType:
  """Collection to use in the tests as destination."""

  coll = mocker.AsyncMock(spec=AsyncCollection)
  type(coll).name = mocker.PropertyMock(return_value="copy")
  return coll


async def test_copy_all(
  mocker: MockerFixture,
  copier: CollCopier,
  coll: AsyncMockType,
  dst_coll: AsyncMockType,
  cc_records: list[dict],
  cc_record_batches: list[dict],
  default_batch_size: int,
) -> None:
  """Check that copy_coll() copies all the records."""

  # (1) arrange
  # prepare responses of coll.get() mock
  (get := coll.get).side_effect = [
    {
      "ids": [r["id"] for r in batch],
      "metadatas": [r["metadata"] for r in batch],
      "documents": [r["document"] for r in batch],
    }
    for batch in cc_record_batches
  ] + [  # no more records
    {
      "ids": [],
      "metadatas": [],
      "documents": [],
    }
  ]

  # (2) act
  out = await copier.copy_coll(coll, dst_coll)

  # (3) assessment
  assert out.coll == coll.name
  assert out.dst_coll == dst_coll.name
  assert out.count == len(cc_records)
  assert out.duration >= 0

  assert get.await_args_list == [
    mocker.call(
      include=["metadatas", "documents"],
      where=None,
      offset=i * default_batch_size,
      limit=2,
    )
    for i in range(0, ceil(out.count / default_batch_size) + 1)
  ]
