from abc import ABC
from dataclasses import dataclass


@dataclass
class CollIERpt(ABC):
  """An import/export report related with a collection."""

  coll: str
  """Collection name."""

  count: int
  """Number of records imported, exported or copied."""

  duration: int
  """Operation duration in ms."""
