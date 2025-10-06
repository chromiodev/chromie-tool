from dataclasses import dataclass

from .._rpt import CollIERpt


@dataclass
class CollExportRpt(CollIERpt):
  """Report associated to a collection export."""
