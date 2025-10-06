import pytest


@pytest.fixture(scope="module", autouse=True)
def init(docker_services: None) -> None:
  """Uses pytest-docker automatically in this test hierarchy."""

  pass
