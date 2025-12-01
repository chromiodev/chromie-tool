from asyncio import TaskGroup
from dataclasses import dataclass
from time import time

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._core import Recs
from .._db import CollIEBase
from .producer import RecBatchProducer
from .queue import RecBatchQueue
from .rpt import CollImportRpt
from .writer import RecBatchWriter


@dataclass
class CollImporter(CollIEBase):
  """Imports a collection from file."""

  async def import_coll(
    self,
    coll: AsyncCollection,
    recs: Recs,
    *,
    writers: int = 2,
    remove: list[str] = [],
    set: dict = {},
  ) -> CollImportRpt:
    """Imports the given records in a collection.

    Args:
      coll: Collection to import.
      recs: Records to import.
      writers: Number of consumer/writer workers.
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
        RecBatchProducer(
          queue=q,
          batch_size=self.batch_size,
          remove=remove,
          set=set,
        ).run(recs),
        name="Producer",
      )

      for i in range(writers):
        ct.append(
          cg.create_task(
            RecBatchWriter(queue=q, coll=coll).run(),
            name=f"Consumer #{i + 1}",
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
