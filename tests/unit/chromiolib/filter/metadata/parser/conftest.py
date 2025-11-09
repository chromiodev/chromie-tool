import pytest

from chromio.filter.metadata import MetafilterParser as Parser


@pytest.fixture
def parser() -> Parser:
  """Parser to use in the tests."""

  return Parser()
