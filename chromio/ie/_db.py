from abc import ABC
from dataclasses import dataclass

from .field import Field


@dataclass
class CollIEBase(ABC):
  """Base for the imports or exports to a collection."""

  batch_size: int
  """Maximum number of records that a batch can have in an import/export."""

  fields: list[Field]
  """Record fields to import or export."""
