from enum import StrEnum


class Field(StrEnum):
  """A field name to import or export."""

  id = "ids"
  meta = "metadatas"
  doc = "documents"
  embedding = "embeddings"
