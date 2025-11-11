from dataclasses import dataclass

from chromadb.api.models.AsyncCollection import AsyncCollection

from ..consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from ..field import Field


@dataclass
class CollWriter:
  """A component for writing records into collections."""

  async def write(
    self,
    records: list[dict],
    coll: AsyncCollection,
    *,
    fields=DEFAULT_FIELDS,
    batch_size=DEFAULT_BATCH_SIZE,
    limit: int | None = None,
  ) -> int:
    """Writes data in a collection.

    Args:
      records: Records to write.
      coll: Collection to write.
      fields: Fields to write. id and doc always.
      batch_size: Number of records to write in every batch.
      limit: Maximum number of records to write. If None, all of them.

    Returns:
      The number of records written.
    """

    # (1) determine maximum number of records to write
    size = len(records)
    max = size if limit is None or limit > size else limit

    # (2) write batch by batch
    for i in range(0, max, batch_size):
      # determine j (batch end)
      if (j := i + batch_size) > max:
        j = max

      # write batch
      batch = records[i:j]

      await coll.add(
        ids=[r["id"] for r in batch],
        documents=[r["document"] for r in batch],
        metadatas=[r["metadata"] for r in batch] if Field.meta in fields else None,
        embeddings=[r["embedding"] for r in batch] if Field.embedding in fields else None,
      )

    # (3) return
    return max
