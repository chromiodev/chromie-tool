from math import ceil
from typing import Any

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
  cc_records: list[dict[str, Any]],
  default_batch_size: int,
) -> None:
  """Check that import() imports all the records."""

  # (1) arrange
  # prepare responses of coll.add() mock
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(coll, cc_records)

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == (cc_count := len(cc_records))
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)


async def test_import_all_removing_metadata(
  importer: CollImporter,
  coll: AsyncMockType,
  cc_records: list[dict[str, Any]],
  default_batch_size: int,
) -> None:
  """Check that import() imports the records w/o some metafields."""

  # (1) arrange
  # prepare responses of coll.add() mock
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(coll, cc_records, remove=["cert", "rating"])

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == (cc_count := len(cc_records))
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)

  for call in add.await_args_list:
    assert "cert" not in call.kwargs["metadatas"]


async def test_import_all_setting_metadata(
  importer: CollImporter,
  coll: AsyncMockType,
  cc_records: list[dict[str, Any]],
  default_batch_size: int,
) -> None:
  """Check that import() imports the records w/ some metadata set to other values."""

  # (1) arrange
  # prepare responses of coll.add() mock
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(coll, cc_records, set={"cert": "C", "dir": "D"})

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == (cc_count := len(cc_records))
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)

  for call in add.await_args_list:
    assert call.kwargs["metadatas"][0]["cert"] == "C"
    assert call.kwargs["metadatas"][0]["dir"] == "D"
