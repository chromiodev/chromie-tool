from math import ceil
from pathlib import Path

from pytest_mock import AsyncMockType

from chromio.ie.consts import DEFAULT_FIELDS
from chromio.ie.imp.importer import CollImporter


async def test_import_all(
  coll: AsyncMockType,
  data_dir: Path,
  cc_count: int,
  default_batch_size: int,
) -> None:
  """Check that import() imports all the records."""

  # (1) arrange
  importer = CollImporter(coll=coll, batch_size=default_batch_size, fields=DEFAULT_FIELDS)
  (add := coll.add).return_value = None

  # (2) act
  out = await importer.import_coll(file_path := data_dir / "cc-export.json")

  # (3) assessment
  # report
  assert out.coll == "test"
  assert out.count == cc_count
  assert out.file_path == str(file_path)
  assert out.duration >= 0

  # add mock
  assert add.await_count == ceil(cc_count / default_batch_size)
