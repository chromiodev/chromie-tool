import asyncio
from asyncio import QueueShutDown
from dataclasses import dataclass, field
from typing import Any, Callable, cast

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._writer import RecBatchWriter as RecBatchWriterBase
from ..consts import DEFAULT_FIELDS
from ..field import Field


@dataclass
class RecBatchWriter(RecBatchWriterBase):
  """A worker for inserting record batches into a Chroma collection
  from an asynchronous queue.
  """

  coll: AsyncCollection
  """Collection where to import."""

  fields: list[Field] = field(default_factory=lambda: DEFAULT_FIELDS)
  """Record fields to write."""

  async def run(self, p: Callable[..., None]) -> tuple[int, int]:
    """Runs the writer, dequeuing and writing the records in batches.

    Args:
      p: Function to use for printing the progress.

    Returns:
      (number of batches performed, number of records written).
    """

    # (1) prepare working context
    name: str = cast(Any, asyncio.current_task()).get_name()
    coll, fields, q = self.coll, self.fields, self.queue

    # (2) write batches
    count, batches = 0, 0

    try:
      while True:
        batch = await q.get()
        batches += 1

        p(f"{name}: writing record batch #{batches}...")

        await coll.add(
          ids=[r["id"] for r in batch],
          documents=[r["document"] for r in batch],
          metadatas=[r["metadata"] for r in batch] if Field.meta in fields else None,
          embeddings=[r["embedding"] for r in batch]
          if Field.embedding in fields
          else None,
        )

        q.task_done()
        count += len(batch)
    except QueueShutDown:
      pass

    # (3) return
    return (batches, count)
