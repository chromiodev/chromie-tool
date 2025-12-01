from asyncio import QueueShutDown
from dataclasses import dataclass, field

from chromadb.api.models.AsyncCollection import AsyncCollection

from ..consts import DEFAULT_FIELDS
from ..field import Field
from .queue import RecBatchQueue


@dataclass
class RecBatchWriter:
  """A worker for writing record batches to a Chroma collection asynchronously."""

  queue: RecBatchQueue
  """Asynchronous queue with the record batches to import."""

  coll: AsyncCollection
  """Collection where to import."""

  fields: list[Field] = field(default_factory=lambda: DEFAULT_FIELDS)
  """Record fields to write."""

  async def run(self) -> tuple[int, int]:
    """Dequeues and writes record batches.

    Returns:
      (number of batches performed, number of records written).
    """

    # (1) write batches
    count, batches = 0, 0
    coll, fields, q = self.coll, self.fields, self.queue

    try:
      while True:
        batch = await q.get()

        await coll.add(
          ids=[r["id"] for r in batch],
          documents=[r["document"] for r in batch],
          metadatas=[r["metadata"] for r in batch] if Field.meta in fields else None,
          embeddings=[r["embedding"] for r in batch]
          if Field.embedding in fields
          else None,
        )

        q.task_done()
        batches += 1
        count += len(batch)
    except QueueShutDown:
      pass

    # (2) return number of records written
    return (batches, count)
