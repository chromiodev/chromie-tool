from math import ceil
from pathlib import Path

import pytest
from pytest_mock import AsyncMockType

from chromio.ie.consts import DEFAULT_FIELDS
from chromio.ie.imp.importer import CollImporter


@pytest.fixture(scope="module")
def importer(default_batch_size: int) -> CollImporter:
  """Exporter to use in the tests."""

  return CollImporter(batch_size=default_batch_size, fields=DEFAULT_FIELDS)


async def test_import_all(
  importer: CollImporter,
  coll: AsyncMockType,
  data_dir: Path,
  cc_count: int,
  default_batch_size: int,
) -> None:
  """Check that import() imports all the records."""

  # (1) arrange
  # prepare responses of coll.add() mock
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(coll, file_path := data_dir / "cc-export.json")

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == cc_count
  assert out.file_path == str(file_path)
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)


async def test_import_all_removing_metafields(
  importer: CollImporter,
  coll: AsyncMockType,
  data_dir: Path,
  cc_count: int,
  default_batch_size: int,
) -> None:
  """Check that import() imports all the records, but removing some fields."""

  # (1) arrange
  # prepare responses of coll.add() mock
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(
    coll, file_path := data_dir / "cc-export.json", remove=["cert", "rating"]
  )

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == cc_count
  assert out.file_path == str(file_path)
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)

  for call in add.await_args_list:
    assert "cert" not in call.kwargs["metadatas"]
