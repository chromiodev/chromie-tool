import pytest
from chromadb.api import AsyncClientAPI

from chromio.client import client
from chromio.uri import ChromioUri


@pytest.mark.readonly
@pytest.mark.attr(id="ITG-CL-01")
async def test_server_client() -> None:
  """Check that client() returns a asynchronous client."""

  # (1) act
  out = await client(ChromioUri.server())

  # (2) assessment
  assert isinstance(out, AsyncClientAPI)
