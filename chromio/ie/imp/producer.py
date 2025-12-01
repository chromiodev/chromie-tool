from dataclasses import dataclass, field
from itertools import batched

from .._core import Recs
from .queue import RecBatchQueue


@dataclass
class RecBatchProducer:
  """A worker for producing the record batches into the queue.

  When the records are read, these are adapted to the user requirements.
  For example, remove metadata if needed. So, the writers only write.
  """

  queue: RecBatchQueue
  """Asynchronous queue where to insert the record batches."""

  batch_size: int = 250
  """Size for the record batches to enqueue."""

  remove: list[str] = field(default_factory=list)
  """Metadata to remove in the import."""

  set: dict = field(default_factory=dict)
  """Metadata to set/override in the import."""

  async def run(self, recs: Recs) -> None:
    """Runs the reader.

    Args:
      recs: Records to process.
    """

    # (1) produce the record batches
    remove, set = self.remove, self.set
    bs = self.batch_size

    for batch in batched(recs, bs):
      # remove/set metafields if needed
      if len(remove) > 0 or len(set) > 0:
        for rec in batch:
          md = rec["metadata"]

          for key in remove:
            del md[key]

          for key, val in set.items():
            md[key] = val

      # enqueue batch
      await self.queue.put(batch)

    # (2) close de queue
    self.queue.shutdown()
