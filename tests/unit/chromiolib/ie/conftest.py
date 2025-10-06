import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest_mock import AsyncMockType, MockerFixture


@pytest.fixture(scope="function")
def coll(mocker: MockerFixture) -> AsyncMockType:
  """Collection to use in the tests."""

  coll = mocker.AsyncMock(spec=AsyncCollection)
  type(coll).name = mocker.PropertyMock(return_value="test")
  return coll
