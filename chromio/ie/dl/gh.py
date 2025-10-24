from typing import override

from .http import FILE_EXT, FILE_NAME, HttpDownloader


class GhDownloader(HttpDownloader):
  """A component for downloading dataset files from a GitHub repository."""

  # @override
  base = "https://github.com"

  owner = "chromiodev"
  """Owner repository with the datasets."""

  repo = "datasets"
  """Repository name with the datasets."""

  @override
  def _build_url(self, path: str, lang: str) -> str:
    return f"{self.base}/{self.owner}/{self.repo}/{path}/{FILE_NAME}-{lang}{FILE_EXT}"
