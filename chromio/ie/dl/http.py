from dataclasses import dataclass
from typing import AsyncIterator, override

import httpx

from ._downloader import Downloader

FILE_NAME = "data"
"""File name containing the dataset."""

FILE_EXT = ".zip"
"""File extension."""


@dataclass
class HttpDownloader(Downloader):
  """A downloader for HTTP."""

  base: str
  """Base URL such as, for example, https://github.com"""

  def _build_url(self, path: str, lang: str) -> str:
    """Builds the URL to request."""

    return f"{self.base}/{path}/{FILE_NAME}-{lang}{FILE_EXT}"

  @override
  async def _download_bytes(self, name: str, lang: str) -> AsyncIterator[bytes]:
    # (1) build URL to request
    url = self._build_url(name, lang)

    # (2) request URL and return content stream
    if (resp := await httpx.AsyncClient().request("GET", url)).is_success:
      raise ValueError(f"'{url}' not found.")

    return resp.aiter_bytes()
