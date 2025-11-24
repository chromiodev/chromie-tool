from pathlib import Path
from typing import cast

import pytest
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import CaptureFixture, Pytester


@pytest.mark.usefixtures("truncate_coll")
@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-01")
async def test_import_into_empty_coll(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  coll: AsyncCollection,
  cc_records: list[dict],
) -> None:
  """Check that 'chromie imp' imports into an empty collection."""

  # (1) precondition
  assert await coll.count() == 0

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run("chromie", "imp", input_file, "server://///pytest")
  capsys.readouterr()

  # (4) assessment
  count = len(cc_records)

  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      f"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # coll content
  assert await coll.count() == count


@pytest.mark.usefixtures("arrange_coll")
@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-02")
async def test_import_into_nonempty_coll(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  coll: AsyncCollection,
  qt_records: list[dict],
  cc_records: list[dict],
) -> None:
  """Check that 'chromie imp' imports into a non-empty existing collection."""

  # (1) precondition: only the QT movies are in the coll
  assert await coll.count() == len(qt_records)

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run("chromie", "imp", input_file, "server://///pytest")
  capsys.readouterr()

  # (4) assessment
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      f"Count: {len(cc_records)}",
      r"Duration \(s\): .+",
    ),
  )


@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-03")
async def test_import_into_non_existing_coll(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  db: AsyncClientAPI,
  cc_count: int,
) -> None:
  """Check that 'chromie imp' imports into a non-existent collection."""

  coll_name = "pytest_fn_imp_03"

  # (1) precondition: the collection does not exist
  try:
    await db.delete_collection(coll_name)
  except Exception:
    pass

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run("chromie", "imp", input_file, f"server://///{coll_name}")
  capsys.readouterr()

  # (4) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random(
    (
      f"Collection: {coll_name}",
      f"Count: {cc_count}",
      r"Duration \(s\): .+",
    ),
  )

  # (5) cleanup
  await db.delete_collection(coll_name)


@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-04")
def test_import_into_unknown_server(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
) -> None:
  """Check that 'chromie imp' shows an error if the server is not reachable."""

  # (1) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (2) act
  out = pytester.run(
    "chromie",
    "imp",
    input_file,
    "server://unknown:8000///pytest",
  )
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 1
  out.stderr.re_match_lines((r".*failure.*",))


@pytest.mark.usefixtures("truncate_coll")
@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-05")
async def test_import_removing_metafields(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  coll: AsyncCollection,
  cc_records: list[dict],
) -> None:
  """Check that 'chromie imp -M' doesn't import the given metadata."""

  # (1) precondition
  assert await coll.count() == 0
  assert "rating" in (rec := cc_records[0])["metadata"]

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run(
    "chromie", "imp", "-M", "cert,rating", input_file, "server://///pytest"
  )
  capsys.readouterr()

  # (4) assessment
  count = len(cc_records)

  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      f"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # coll content
  assert await coll.count() == count
  assert "rating" not in cast(dict, await coll.get(rec["id"]))["metadatas"][0]


@pytest.mark.usefixtures("truncate_coll")
@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-06")
async def test_import_setting_metafields(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  coll: AsyncCollection,
  cc_records: list[dict],
) -> None:
  """Check that 'chromie imp -m' imports setting/overwriting metafields."""

  # (1) precondition
  assert await coll.count() == 0
  assert (rec := cc_records[0])["metadata"]["cert"] != "C"
  assert "dir" not in (rec := cc_records[0])["metadata"]

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run(
    "chromie", "imp", "-m", "cert:C,dir:D", input_file, "server://///pytest"
  )
  capsys.readouterr()

  # (4) assessment
  count = len(cc_records)

  # terminal
  assert out.ret == 0

  out.stdout.re_match_lines_random(
    (
      r"Collection: pytest",
      f"Count: {count}",
      r"Duration \(s\): .+",
    ),
  )

  # coll content
  assert await coll.count() == count
  assert (md := cast(dict, await coll.get(rec["id"]))["metadatas"][0])["cert"] == "C"
  assert md["dir"] == "D"


@pytest.mark.readonly
@pytest.mark.attr(id="FN-IMP-07")
async def test_import_into_non_existing_coll_with_conf_passed(
  data_dir: Path,
  pytester: Pytester,
  capsys: CaptureFixture,
  db: AsyncClientAPI,
  cc_count: int,
) -> None:
  """Check that 'chromie imp' imports into a non-existent collection, creating the collection
  with the embedding function passed.
  """

  coll_name = "pytest_fn_imp_07"

  # (1) precondition: the collection does not exist
  try:
    await db.delete_collection(coll_name)
  except Exception:
    pass

  # (2) arrange
  input_file = pytester.copy_example(str(data_dir / "cc-export.json"))

  # (3) act
  out = pytester.run(
    "chromie", "imp", "--efn=sentence_transformer", input_file, f"server://///{coll_name}"
  )
  capsys.readouterr()

  # (4) assessment
  # term
  assert out.ret == 0
  out.stdout.re_match_lines_random(
    (
      f"Collection: {coll_name}",
      f"Count: {cc_count}",
      r"Duration \(s\): .+",
    ),
  )

  # db
  coll = await db.get_collection(coll_name)
  assert coll.configuration_json["embedding_function"]["name"] == "sentence_transformer"
  assert (await coll.count()) == cc_count

  # (5) cleanup
  await db.delete_collection(coll_name)
