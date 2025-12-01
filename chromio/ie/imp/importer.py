from asyncio import TaskGroup
from dataclasses import dataclass
from pathlib import Path
from time import time

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._db import CollIEBase
from .queue import RecBatchQueue
from .reader import RecBatchReader
from .rpt import CollImportRpt
from .writer import RecBatchWriter


@dataclass
class CollImporter(CollIEBase):
  """Imports a collection from file."""

  async def import_coll(
    self,
    coll: AsyncCollection,
    file_path: Path,
    *,
    writers: int = 2,
    limit: int | None = None,
    remove: list[str] = [],
    set: dict = {},
  ) -> CollImportRpt:
    """Imports the given records in a collection.

    Args:
      coll: Collection to import.
      file_path: Path to the JSONL file with the records.
      writers: Number of consumer/writer workers.
      limit: Maximum number of records to import.
      remove: Metadata to remove in the import.
      set: Metadata to set/override in the import.

    Returns:
      An import report.
    """

    # (1) prepare
    start = time()
    q = RecBatchQueue()

    # (2) import
    ct = []  # consumer tasks

    async with TaskGroup() as pg, TaskGroup() as cg:
      pg.create_task(
        RecBatchReader(
          queue=q,
          file_path=file_path,
          limit=limit,
          batch_size=self.batch_size,
          remove=remove,
          set=set,
        ).run(),
        name="JSONL file reader",
      )

      for i in range(writers):
        ct.append(
          cg.create_task(
            RecBatchWriter(queue=q, coll=coll).run(),
            name=f"Record batch writer #{i + 1}",
          )
        )

      await q.join()

    # (3) generate the report
    return CollImportRpt(
      coll=coll.name,
      batches=sum(t.result()[0] for t in ct),
      count=sum(t.result()[1] for t in ct),
      duration=int(time() - start),
    )
