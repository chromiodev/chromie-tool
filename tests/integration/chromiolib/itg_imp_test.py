from typing import Any

import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection

from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from chromio.ie.imp.importer import CollImporter


@pytest.fixture(scope="module")
def importer() -> CollImporter:
  """Importer to use in the tests."""

  return CollImporter(batch_size=DEFAULT_BATCH_SIZE, fields=DEFAULT_FIELDS)


@pytest.mark.attr(id="ITG-IMP-01")
@pytest.mark.usefixtures("truncate_coll")
async def test_import_all_records(
  importer: CollImporter,
  coll: AsyncCollection,
  cc_records: list[dict[str, Any]],
) -> None:
  """Check that CollImporter.import_coll() imports all the records from the file."""

  # (1) precondition: the collection must not contain records
  assert await coll.count() == 0

  # (2) act
  out = await importer.import_coll(coll, cc_records)

  # (3)) assessment
  # report
  assert out.coll == coll.name
  assert out.count == (cc_count := len(cc_records))

  # collection
  assert await coll.count() == cc_count


@pytest.mark.attr(id="ITG-IMP-02")
@pytest.mark.usefixtures("truncate_coll")
async def test_import_with_limit(
  importer: CollImporter,
  coll: AsyncCollection,
  cc_records: list[dict[str, Any]],
) -> None:
  """Check that CollImporter.import_coll() imports the maximum number of records set."""

  limit = 2

  # (1) precondition: the collection must not contain records
  assert await coll.count() == 0
  assert len(cc_records) > limit

  # (2) act
  out = await importer.import_coll(coll, cc_records, limit=limit)

  # (3) assessment
  # report
  assert out.coll == coll.name
  assert out.count == limit

  # collection
  assert await coll.count() == limit
