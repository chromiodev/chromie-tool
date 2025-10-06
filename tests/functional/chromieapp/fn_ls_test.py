import pytest
from chromadb.api import AsyncClientAPI
from pytest import CaptureFixture, Pytester

# Implicit pytest marks.
pytestmark = [pytest.mark.usefixtures("arrange_coll")]


@pytest.mark.readonly
@pytest.mark.attr(id="FN-LS-01")
@pytest.mark.usefixtures("arrange_coll2")
async def test_list_names(
  pytester: Pytester, capsys: CaptureFixture, db: AsyncClientAPI
) -> None:
  """Check that 'chromie ls' prints the collection names."""

  # (1) precondition
  assert len(colls := await db.list_collections()) == 2

  # (2) act
  out = pytester.run("chromie", "ls", "server:////")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  assert len(out.stdout.lines) == len(colls)


@pytest.mark.readonly
@pytest.mark.attr(id="FN-LS-02")
@pytest.mark.usefixtures("arrange_coll2")
async def test_list_names_and_counts(
  pytester: Pytester, capsys: CaptureFixture, db: AsyncClientAPI
) -> None:
  """Check that 'chromie ls' prints the collection names and their counts."""

  # (1) precondition
  assert len(colls := await db.list_collections()) == 2

  # (2) act
  out = pytester.run("chromie", "ls", "server:////", "-c")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  assert len(out.stdout.lines) == len(colls)
  out.stdout.re_match_lines(r"^.+: \d+$")


@pytest.mark.readonly
@pytest.mark.attr(id="FN-LS-03")
async def test_attempt_to_list_unknown_db(
  pytester: Pytester, capsys: CaptureFixture
) -> None:
  """Check that 'chromie ls' prints error if unknown db."""

  # (1) act
  out = pytester.run("chromie", "ls", "server:////db")
  capsys.readouterr()

  # (2) assessment
  assert out.ret == 1
  out.stderr.re_match_lines(r".*not found.*")
