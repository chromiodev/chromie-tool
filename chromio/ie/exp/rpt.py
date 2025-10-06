from dataclasses import dataclass

from .._rpt import CollIERpt


@dataclass
class CollExportRpt(CollIERpt):
  """Report associated to a collection export."""

  file_path: str
  """File path where the data saved."""
