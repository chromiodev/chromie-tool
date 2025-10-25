from pathlib import Path

import pytest
from aiofiles import ospath as path

from chromio.ie.dl import Downloader
from chromio.ie.dl.http import HttpDownloader


@pytest.fixture
def dl() -> Downloader:
  """Downloader to use in the tests."""

  return HttpDownloader(base="https://raw.githubusercontent.com")


async def test_download_existing_dataset(tmp_path: Path, dl: Downloader) -> None:
  """Check that the download() method downloads an existing dataset."""

  # (1) arrange
  dst = tmp_path / "prc_hicp_manr.json"

  # (2) act
  out = await dl.download("chromiodev/datasets/main/eurostat/prc_hicp_manr", dst)

  # (3) assessment
  assert out is None
  assert await path.isfile(dst)
