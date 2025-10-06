import pytest
from pytest import MonkeyPatch

from chromio.uri import ChromioUri, parse_uri


def test_parse_invalid_uri_schema() -> None:
  """Check that parse_uri() raises ValueError if invalid schema."""

  with pytest.raises(ValueError, match="Invalid URI schema: 'p:///dir'."):
    parse_uri("p:///dir")


###########
# path:// #
###########


def test_parse_valid_path_uri() -> None:
  """Check that parse_uri() returns a valid path URI."""

  # (1) act
  out = parse_uri("path:///tmp/dir")

  # (2) assessment
  assert isinstance(out, ChromioUri)
  assert out == ChromioUri(schema="path", path="/tmp/dir")


#############
# server:// #
#############


@pytest.mark.parametrize(
  ("uri", "e"),
  (
    pytest.param(
      "server:////",
      ChromioUri.server(),
      id="server:////",
    ),
    pytest.param(
      "server://///collname",
      ChromioUri.server(coll="collname"),
      id="server://///collname",
    ),
    pytest.param(
      "server://localhost:8000/user/dbname",
      ChromioUri.server(host="localhost", port=8000, tenant="user", db="dbname"),
      id="server://localhost:8000/user/dbname",
    ),
    pytest.param(
      "server://localhost:8000/user/dbname/collname",
      ChromioUri.server(
        host="localhost", port=8000, tenant="user", db="dbname", coll="collname"
      ),
      id="server://localhost:8000/user/dbname/collname",
    ),
    pytest.param(
      "server://localhost//",
      ChromioUri.server(host="localhost", port=8000),
      id="server://localhost//",
    ),
    pytest.param(
      "server://localhost///collname",
      ChromioUri.server(host="localhost", port=8000, coll="collname"),
      id="server://localhost///collname",
    ),
    pytest.param(
      "server://localhost/user/dbname",
      ChromioUri.server(host="localhost", port=8000, tenant="user", db="dbname"),
      id="server://localhost/user/dbname",
    ),
    pytest.param(
      "server://localhost/user/dbname/collname",
      ChromioUri.server(
        host="localhost", port=8000, tenant="user", db="dbname", coll="collname"
      ),
      id="server://localhost/user/dbname/collname",
    ),
  ),
)
def test_parse_valid_server_uri(uri: str, e: ChromioUri) -> None:
  """Check that parse_uri() returns a valid server URI."""

  assert parse_uri(uri) == e


@pytest.mark.parametrize(
  ("uri",),
  (
    pytest.param("server://"),
    pytest.param("server:///"),
  ),
)
def test_parse_invalid_server_uri(uri: str) -> None:
  """Check that parse_uri() raises error if invalid URI."""

  with pytest.raises(ValueError, match=f"Invalid server URI: '{uri}'."):
    parse_uri(uri)


############
# cloud:// #
############


@pytest.mark.parametrize(
  ("uri", "coll", "env"),
  (
    pytest.param(
      "cloud:///user/dbname",
      None,
      {},
      id="explicit tenant and db",
    ),
    pytest.param(
      "cloud:///user/dbname/collname",
      "collname",
      {},
      id="all explicit",
    ),
    pytest.param(
      "cloud:////dbname",
      None,
      {"CHROMA_TENANT": "user"},
      id="CHROMA_TENANT",
    ),
    pytest.param(
      "cloud:////dbname/collname",
      "collname",
      {"CHROMA_TENANT": "user"},
      id="CHROMA_TENANT",
    ),
    pytest.param(
      "cloud:///user/",
      None,
      {"CHROMA_DATABASE": "dbname"},
      id="CHROMA_DATABASE",
    ),
    pytest.param(
      "cloud:///user//collname",
      "collname",
      {"CHROMA_DATABASE": "dbname"},
      id="CHROMA_DATABASE",
    ),
  ),
)
def test_parse_valid_cloud_uri(
  monkeypatch: MonkeyPatch, uri: str, coll: str | None, env: dict[str, str]
) -> None:
  """Check that parse_uri() returns a valid cloud URI."""

  # (1) arrange
  for v in env:
    monkeypatch.setenv(v, env[v])

  # (2) act
  out = parse_uri(uri)

  # (3) assessment
  assert out == ChromioUri(
    schema="cloud",
    host="api.trychroma.com",
    port=8000,
    tenant="user",
    db="dbname",
    coll=coll,
  )


@pytest.mark.parametrize(
  ("uri",),
  (
    pytest.param("cloud://"),
    pytest.param("cloud:///"),
  ),
)
def test_parse_invalid_cloud_uri(uri: str) -> None:
  """Check that parse_uri() raises error if invalid URI."""

  with pytest.raises(ValueError, match=f"Invalid cloud URI: '{uri}'."):
    parse_uri(uri)


@pytest.mark.parametrize(
  ("uri", "e"),
  (
    pytest.param("cloud:///tenant/", "/tenant/"),
    pytest.param("cloud:////db", "//db"),
  ),
)
def test_parse_cloud_uri_missing_tenant_or_db(uri: str, e: str) -> None:
  with pytest.raises(ValueError, match=f"Expected tenant and db in cloud URI: '{e}'."):
    parse_uri(uri)
