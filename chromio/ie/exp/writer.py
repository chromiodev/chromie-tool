import asyncio
from asyncio import QueueShutDown
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, cast

from aiofiles import open

from .._writer import RecBatchWriter
from . import jsonl


@dataclass
class RecFileWriter(RecBatchWriter):
  """A worker for inserting record batches into a file from an asynchronous queue."""

  file_path: Path
  """Path to the file where to save the records."""

  async def run(self, p: Callable[..., None]) -> tuple[int, int]:
    """Runs the writer, dequeuing and writing the records in batches.

    Args:
      p: Function to use for printing the progress.

    Returns:
      (number of batches performed, number of records written).
    """

    # (1) prepare context
    name: str = cast(Any, asyncio.current_task()).get_name()

    # (2) write batches
    count, batches = 0, 0
    q = self.queue

    async with open(self.file_path, "w", encoding="utf-8") as f:
      try:
        while True:
          batch = await q.get()
          batches += 1

          p(f"{name}: writing record batch #{batches}...")

          await f.writelines(
            [
              "\n" if count > 0 else "",
              jsonl.dumps(batch, indent=0, sep="\n"),
              "",
            ]
          )

          q.task_done()
          count += len(batch)
      except QueueShutDown:
        pass

    # (3) return number of records written
    return (batches, count)
