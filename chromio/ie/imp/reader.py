import json
from dataclasses import dataclass, field
from pathlib import Path

from aiofiles import open

from .._reader import RecBatchReader
from ..consts import DEFAULT_BATCH_SIZE


@dataclass
class RecFileReader(RecBatchReader):
  """A worker for reading a JSONL with Chroma records and producing its batches
  to an asynchronous queue.

  When the records are read, these are adapted to the user requirements.
  For example, remove metadata if needed. So, the writers only write.
  """

  file_path: Path
  """Path to the JSONL file with the records."""

  limit: int | None = None
  """Maximum number of records to read/produce."""

  batch_size: int = DEFAULT_BATCH_SIZE
  """Size for the record batches to enqueue."""

  remove: list[str] = field(default_factory=list)
  """Metadata to remove in the import."""

  set: dict = field(default_factory=dict)
  """Metadata to set/override in the import."""

  async def run(self) -> None:
    """Runs the reader."""

    # (1) prepare context
    q, batch_size, limit = self.queue, self.batch_size, self.limit
    remove, set = self.remove, self.set

    # (2) read batch by batch
    async with open(self.file_path, "r", encoding="utf-8") as f:
      count = 0
      batch = []

      # read line by line creating batches
      async for ln in f:
        if ln.strip():
          # pre: limit not reached
          if (count := count + 1) and limit is not None and count > limit:
            break

          # prepare record and remove/set metafields if needed
          rec = json.loads(ln)

          if len(remove) > 0 or len(set) > 0:
            md = rec["metadata"]

            for key in remove:
              del md[key]

            for key, val in set.items():
              md[key] = val

          # add record to batch
          batch.append(rec)

          # added to a queue when batch size reached
          if len(batch) >= batch_size:
            await q.put(batch)
            batch = []

      # add last batch when reached EOF with batch size not reached
      if len(batch) > 0:
        await q.put(batch)

    # (3) close de queue
    q.shutdown()
