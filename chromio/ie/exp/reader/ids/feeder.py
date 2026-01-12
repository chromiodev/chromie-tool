from dataclasses import dataclass

from chromadb.api.models.AsyncCollection import AsyncCollection

from ....consts import DEFAULT_BATCH_SIZE
from .queue import IdBatchQueue


@dataclass
class IdBatchFeeder:
  """A worker for reading the identifiers of a collection in batches,
  putting into an asynchronous queue.
  """

  coll: AsyncCollection
  """Collection to read."""

  queue: IdBatchQueue
  """Queue where to save the id batches."""

  batch_size: int = DEFAULT_BATCH_SIZE
  """Size of the id batches to feed."""

  limit: int | None = None
  """Maximum number of ids to feed."""

  metafilter: dict | None = None
  """Metadata filter to apply for getting the ids to export."""

  async def run(self) -> None:
    """Runs the id feeder."""

    # (1) prepare working context
    batch_size, limit = self.batch_size, self.limit
    metafilter = self.metafilter
    coll, q = self.coll, self.queue

    # (2) read/produce the batches
    batch_no, ended = 0, False

    while not ended:
      # set offset and batch size (the last one can be less than this passed)
      offset = batch_no * batch_size

      if limit is not None and offset + batch_size >= limit:
        ended, batch_size = True, limit - offset

      # read next batch, exiting if no more records
      if (
        len(
          batch := (
            await coll.get(include=[], where=metafilter, offset=offset, limit=batch_size)
          )["ids"]
        )
      ) == 0:
        break

      batch_no += 1

      # enqueue id batch
      await q.put(batch)

    # (3) close queue
    q.shutdown()
