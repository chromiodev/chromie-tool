import json

import pytest
from aiofiles import open
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import Pytester

from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from chromio.ie.exp import CollExporter


@pytest.fixture(scope="module")
def exporter() -> CollExporter:
  """Exporter to use in the tests."""

  return CollExporter(batch_size=DEFAULT_BATCH_SIZE, fields=DEFAULT_FIELDS)


@pytest.mark.readonly
@pytest.mark.attr(id="ITG-EXP-01")
@pytest.mark.usefixtures("arrange_coll")
async def test_export_coll_fully(
  pytester: Pytester, exporter: CollExporter, db: AsyncClientAPI, coll: AsyncCollection
) -> None:
  """Check that CollExporter.export_coll() performs this expected."""

  # (1) precondition: collection has at least two records
  assert (count := await coll.count()) > 2

  # (2) arrange
  v = await db.get_version()
  outfile = pytester.makefile(".json", export="")

  # (3) act
  out = await exporter.export_coll(coll, outfile, v=v)

  # (4) assessment
  # report
  assert out.coll == coll.name
  assert out.count == count
  assert out.file_path == str(outfile)

  # export file
  async with open(outfile, mode="r") as f:
    assert len(data := json.loads(await f.read())["data"]) == count

  for r in data:
    assert "id" in r
    assert "metadata" in r
    assert "document" in r


@pytest.mark.readonly
@pytest.mark.attr(id="ITG-EXP-02")
@pytest.mark.usefixtures("arrange_coll")
async def test_export_coll_partially(
  pytester: Pytester, exporter: CollExporter, db: AsyncClientAPI, coll: AsyncCollection
) -> None:
  """Check that CollExporter.export_coll() performs this expected when limit set."""

  # (1) precondition: collection has at least three records
  assert await coll.count() >= 3

  # (2) arrange
  limit = 2
  outfile = pytester.makefile(".json", export="")
  v = await db.get_version()

  # (3) act
  out = await exporter.export_coll(coll, outfile, v=v, limit=limit)

  # (4) assessment
  # report
  assert out.coll == coll.name
  assert out.count == limit
  assert out.file_path == str(outfile)

  # export file
  async with open(outfile, mode="r") as f:
    assert len(data := json.loads(await f.read())["data"]) == limit

  for r in data:
    assert "id" in r
    assert "metadata" in r
    assert "document" in r
