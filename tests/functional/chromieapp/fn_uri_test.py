import pytest
from pytest import CaptureFixture, MonkeyPatch, Pytester


@pytest.mark.readonly
@pytest.mark.attr(id="FN-URI-01")
async def test_valid_server_uri(
  pytester: Pytester, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
  """Check that 'chromie uri' prints the segments of a server URI."""

  # (1) precondition
  monkeypatch.setenv("CHROMA_PORT", "8008")

  # (2) act
  out = pytester.run("chromie", "uri", "server:////")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  out.stdout.fnmatch_lines(
    (
      "Schema: server",
      "Host: localhost",
      "Port: 8008",
      "Tenant: default_tenant",
      "Database: default_database",
    )
  )


@pytest.mark.readonly
@pytest.mark.attr(id="FN-URI-02")
async def test_valid_cloud_uri(
  pytester: Pytester, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
  """Check that 'chromie uri' prints the segments of a cloud URI."""

  # (1) precondition
  monkeypatch.setenv("CHROMA_TENANT", "my_tenant")
  monkeypatch.setenv("CHROMA_DATABASE", "my_database")

  # (2) act
  out = pytester.run("chromie", "uri", "cloud:////")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 0
  out.stdout.fnmatch_lines(
    (
      "Schema: cloud",
      "Host: api.trychroma.com",
      "Port: 8000",
      "Tenant: my_tenant",
      "Database: my_database",
    )
  )


@pytest.mark.readonly
@pytest.mark.attr(id="FN-URI-02")
async def test_invalid_cloud_uri(
  pytester: Pytester, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
  """Check that 'chromie uri' prints error if invalid cloud URI."""

  # (1) precondition
  monkeypatch.delenv("CHROMA_TENANT", raising=False)
  monkeypatch.delenv("CHROMA_DATABASE", raising=False)

  # (2) act
  out = pytester.run("chromie", "uri", "cloud:////")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 1
  out.stderr.re_match_lines_random((".*Expected tenant.*"))
