from math import ceil
from pathlib import Path

import pytest
from aiofiles import open
from pytest_mock import AsyncMockType, MockerFixture

from chromio.ie.consts import DEFAULT_FIELDS
from chromio.ie.exp import CollExporter


@pytest.fixture(scope="module")
def exporter(default_batch_size: int) -> CollExporter:
  """Exporter to use in the tests."""

  return CollExporter(batch_size=default_batch_size, fields=DEFAULT_FIELDS)


async def test_export_all(
  mocker: MockerFixture,
  exporter: CollExporter,
  coll: AsyncMockType,
  tmp_path: Path,
  cc_records: list[dict],
  cc_export: str,
  cc_record_batches: list[dict],
  default_batch_size: int,
) -> None:
  """Check that export() exports all the records."""

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
  out = await exporter.export_coll(coll, file_path := tmp_path / "test.json", v="1.1.0")

  # (3) assessment
  assert out.coll == "test"
  assert out.count == len(cc_records)
  assert out.file_path == str(file_path)
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

  async with open(file_path, "r") as file:
    assert await file.read() == cc_export
