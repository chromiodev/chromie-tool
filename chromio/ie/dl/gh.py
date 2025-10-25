from dataclasses import dataclass
from typing import override

from .http import FILE_EXT, FILE_NAME, HttpDownloader


@dataclass
class GitHubDownloader(HttpDownloader):
  """A component for downloading dataset files from a GitHub repository."""

  # @override
  base: str = "https://raw.githubusercontent.com"

  owner = "chromiodev"
  """Owner repository with the datasets."""

  repo = "datasets"
  """Repository name with the datasets."""

  @override
  def _build_url(self, path: str, lang: str) -> str:
    return (
      f"{self.base}/{self.owner}/{self.repo}/main/{path}/{FILE_NAME}-{lang}{FILE_EXT}"
    )
