from pathlib import Path

import pytest
from aiofiles import ospath as path

from chromio.ie.dl import Downloader
from chromio.ie.dl.gh import GitHubDownloader


@pytest.fixture
def dl() -> Downloader:
  """Downloader to use in the tests."""

  return GitHubDownloader()


async def test_download_existing_dataset(tmp_path: Path, dl: Downloader) -> None:
  """Check that the download() method downloads an existing dataset."""

  # (1) arrange
  dst = tmp_path / "prc_hicp_manr.json"

  # (2) act
  out = await dl.download("eurostat/prc_hicp_manr", dst)

  # (3) assessment
  assert out is None
  assert await path.isfile(dst)


async def test_download_raises_error_if_not_found(tmp_path: Path, dl: Downloader) -> None:
  """Check that the download() method downloads an existing dataset."""

  # (1) arrange
  dst = tmp_path / "prc_hicp_manr.json"

  # (2) act and assessment
  with pytest.raises(FileNotFoundError, match="not found"):
    await dl.download("eurostat/prc_hicp_manr_x", dst)
