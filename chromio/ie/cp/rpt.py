from dataclasses import dataclass

from .._rpt import CollIERpt


@dataclass
class CollCopyRpt(CollIERpt):
  """Report associated to a collection copy."""

  dst_coll: str
  """Collection where the data copied."""
