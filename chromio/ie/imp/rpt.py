from dataclasses import dataclass

from .._rpt import CollIERpt


@dataclass
class CollImportRpt(CollIERpt):
  """Report associated to a collection import."""

  batches: int
  """Number of batches written performed for writing the records."""
