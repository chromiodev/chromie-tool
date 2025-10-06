from abc import ABC
from dataclasses import dataclass


@dataclass
class CollIERpt(ABC):
  """An import/export report related with a collection."""

  coll: str
  """Collection name."""

  count: int
  """Number of records imported or exported."""

  duration: int
  """Import/export duration in ms."""

  file_path: str
  """File path where the data saved or got."""
