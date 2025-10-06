from chromio.uri import ChromioUri


def test_server() -> None:
  """Check that Chromio.server() returns a valid ChromioUri."""

  # (1) act
  out = ChromioUri.server()

  # (2) assessment
  assert out.schema == "server"


def test_cloud() -> None:
  """Check that Chromio.cloud() returns a valid ChromioUri."""

  # (1) act
  out = ChromioUri.cloud()

  # (2) assessment
  assert out.schema == "cloud"
