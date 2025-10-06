from typing import cast

from chromadb import AsyncHttpClient
from chromadb.api import AsyncClientAPI
from chromadb.config import Settings

from chromio.uri import ChromioUri


async def client(uri: ChromioUri, api_key: str | None = None) -> AsyncClientAPI:
  """Creates an asynchronous Chroma client for the given URI.

  Args:
    uri: URI to use for creating the client.
    api_key: API key to use.

  Returns:
    An asynchronous client.
  """

  return await AsyncHttpClient(
    host=cast(str, uri.host),
    port=cast(int, uri.port),
    tenant=cast(str, uri.tenant),
    database=cast(str, uri.db),
    ssl=uri.schema == "cloud",
    headers={"x-chroma-token": api_key} if api_key is not None else {},
    settings=Settings(anonymized_telemetry=False),
  )
