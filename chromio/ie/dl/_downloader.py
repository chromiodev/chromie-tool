from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from aiofiles import open


@dataclass
class Downloader(ABC):
  """A component for downloading Chromie datasets."""

  # @override
  base = "https://github.com"

  async def download(self, name: str, dst: Path, *, lang="en") -> None:
    """Downloads a dataset file.

    Args:
      name: Dataset name such as, for example, a directory path.
      dst: Destination file path.
      lang: Dataset language such as, for example, ES, EN, IT, etc.

    Raises:
      FileNotFoundError: if the dataset file not found.
    """

    async with open(dst, "wb") as f:
      async for chunk in await self._download_bytes(name, lang):
        await f.write(chunk)

  @abstractmethod
  async def _download_bytes(self, name: str, lang: str) -> AsyncIterator[bytes]:
    """Downloads a dataset file returning an asynchronous iterator with the content."""
