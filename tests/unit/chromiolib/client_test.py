from pytest_mock import AsyncMockType, MockerFixture

from chromio.client import client
from chromio.uri import ChromioUri


async def test_server_client(mocker: MockerFixture) -> None:
  """Check that client() returns a asynchronous client."""

  # (1) arrange
  AsyncHttpClient = mocker.patch(
    "chromio.client._client.AsyncHttpClient", new_callable=mocker.AsyncMock
  )

  # (2) act
  out = await client(ChromioUri.server())

  # (3) assessment
  assert isinstance(out, AsyncMockType)
  assert AsyncHttpClient.await_count == 1
