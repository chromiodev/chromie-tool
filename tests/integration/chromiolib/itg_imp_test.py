import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import Pytester

from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from chromio.ie.imp.importer import CollImporter


@pytest.fixture(scope="module")
def importer() -> CollImporter:
  """Importer to use in the tests."""

  return CollImporter(batch_size=DEFAULT_BATCH_SIZE, fields=DEFAULT_FIELDS)


@pytest.mark.attr(id="ITG-IMP-01")
@pytest.mark.usefixtures("truncate_coll")
async def test_import_all_records(
  pytester: Pytester, importer: CollImporter, coll: AsyncCollection, cc_count: int
) -> None:
  """Check that Importer.import_coll() imports all the records from the file."""

  # (1) precondition: the collection must not contain records
  assert await coll.count() == 0

  # (2) arrange
  input_file = pytester.copy_example("tests/data/cc-export.json")

  # (3) act
  out = await importer.import_coll(coll, input_file)

  # (4) assessment
  # report
  assert out.coll == coll.name
  assert out.file_path == str(input_file)
  assert out.count == cc_count

  # collection
  assert await coll.count() == cc_count


@pytest.mark.attr(id="ITG-IMP-02")
@pytest.mark.usefixtures("truncate_coll")
async def test_import_with_limit(
  pytester: Pytester, importer: CollImporter, coll: AsyncCollection, cc_count: int
) -> None:
  """Check that Importer.import_coll() imports the maximum number of records set."""

  limit = 2

  # (1) precondition: the collection must not contain records
  assert await coll.count() == 0
  assert cc_count > limit

  # (2) arrange
  input_file = pytester.copy_example("tests/data/cc-export.json")

  # (3) act
  out = await importer.import_coll(coll, input_file, limit=limit)

  # (4) assessment
  # report
  assert out.coll == coll.name
  assert out.file_path == str(input_file)
  assert out.count == limit

  # collection
  assert await coll.count() == limit
