from dataclasses import dataclass

from .._rpt import CollIERpt


@dataclass
class CollImportRpt(CollIERpt):
  """Report associated to a collection import."""

  file_path: str
  """File path where the data got from."""
