import pytest
from chromadb.api import AsyncClientAPI
from pytest import CaptureFixture, Pytester


@pytest.mark.readonly
@pytest.mark.attr(id="FN-PING-01")
async def test_ping_reachable_server(pytester: Pytester, capsys: CaptureFixture) -> None:
  """Check that 'chromie ping server://' reaches the server instance."""

  # (1) act
  out = pytester.run("chromie", "ping", "server:////")
  capsys.readouterr()

  # (2) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random(("Ping database: ok",))


@pytest.mark.readonly
@pytest.mark.attr(id="FN-PING-02")
async def test_ping_reachable_coll(
  pytester: Pytester, capsys: CaptureFixture, db: AsyncClientAPI
) -> None:
  """Check that 'chromie ping server://///coll' reaches the server instance."""

  # (1) precondition
  coll_name = "pytest"
  await db.get_or_create_collection(name=coll_name)

  # (2) act
  out = pytester.run("chromie", "ping", f"server://///{coll_name}")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random(("Ping database: ok", "Ping collection: ok"))


@pytest.mark.readonly
@pytest.mark.attr(id="FN-PING-03")
async def test_ping_unreachable_server(
  pytester: Pytester, capsys: CaptureFixture
) -> None:
  """Check that 'chromie ping server://' prints error when unreachable server."""

  # (1) act
  out = pytester.run("chromie", "ping", "server://localhost:8888//")
  capsys.readouterr()

  # (2) assessment
  assert out.ret == 1
  out.stderr.re_match_lines_random(("All connection attempts failed",))
