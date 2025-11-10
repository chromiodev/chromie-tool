import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest_mock import AsyncMockType, MockerFixture


@pytest.fixture(scope="function")
def coll(mocker: MockerFixture) -> AsyncMockType:
  """Collection to use in the tests."""

  # (1) create mock
  coll = mocker.AsyncMock(spec=AsyncCollection)
  type(coll).name = mocker.PropertyMock(return_value="test")
  type(coll).configuration = mocker.PropertyMock(
    return_value={
      "embedding_function": (fn := mocker.Mock()),
      "spann": {"space": "cosine"},
    }
  )
  type(fn).name = mocker.Mock(return_value="default")

  # (2) return mock
  return coll
