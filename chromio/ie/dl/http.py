import os
from dataclasses import dataclass
from typing import AsyncIterator, override

import httpx

from ._downloader import Downloader

FILE_NAME = "data"
"""File name containing the dataset."""

FILE_EXT = ".json"
"""File extension."""


@dataclass
class HttpDownloader(Downloader):
  """A downloader for HTTP."""

  base: str
  """Base URL such as, for example, https://github.com"""

  def _build_url(self, path: str, lang: str) -> str:
    """Builds the URL to request."""

    return f"{self.base}/{path}/{FILE_NAME}-{lang}{FILE_EXT}"

  def _build_headers(self) -> dict[str, str]:
    """Builds the HTTP request headers.

    The user must configure the GH_TOKEN environment variable only if this performs
    very much requests. Needed for GitHub Actions too.
    """

    # (1) build the headers
    headers = {}

    if token := os.getenv("GH_TOKEN"):
      headers["Authorization"] = f"Bearer {token}"  # pragma: no cover

    # (2) return the headers
    return headers

  @override
  async def _download_bytes(self, name: str, lang: str) -> AsyncIterator[bytes]:
    # (1) build URL to request
    url = self._build_url(name, lang)

    # (2) request URL and return content stream
    if not (
      resp := await httpx.AsyncClient().request("GET", url, headers=self._build_headers())
    ).is_success:
      raise FileNotFoundError(f"'{url}' not found.")

    return resp.aiter_bytes()
