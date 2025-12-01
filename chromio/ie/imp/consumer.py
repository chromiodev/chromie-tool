from asyncio import QueueShutDown
from dataclasses import dataclass, field

from chromadb.api.models.AsyncCollection import AsyncCollection

from .queue import RecBatchQueue
from .writer import CollWriter


@dataclass
class RecBatchConsumer:
  """A worker for writing record batches to a Chroma collection asynchronously."""

  queue: RecBatchQueue
  """Asynchronous queue with the record batches to import."""

  coll: AsyncCollection
  """Collection where to import."""

  writer: CollWriter = field(init=False, default_factory=CollWriter)
  """Writer to use for writing the records."""

  async def run(self) -> int:
    """Dequeues and writes record batches.

    Returns:
      Number of records written.
    """

    # (1) write batches
    count = 0
    q = self.queue

    try:
      while True:
        count += await self.writer.write(await q.get(), self.coll)
        q.task_done()
    except QueueShutDown:
      pass

    # (2) return number of records written
    return count
