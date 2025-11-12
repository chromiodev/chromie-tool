import json

import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest_mock import AsyncMockType, MockerFixture


@pytest.fixture(scope="function")
def coll(mocker: MockerFixture, cc_export: str) -> AsyncMockType:
  """Collection to use in the tests."""

  # (1) create mock
  coll = mocker.AsyncMock(spec=AsyncCollection)
  type(coll).name = mocker.PropertyMock(return_value="test")
  type(coll).configuration_json = mocker.PropertyMock(
    return_value=json.loads(cc_export)["metadata"]["coll"]["configuration"]
  )

  # (2) return mock
  return coll
