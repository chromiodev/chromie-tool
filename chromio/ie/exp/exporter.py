import json
from asyncio import TaskGroup
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Callable

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._db import CollIEBase
from .._queue import RecBatchQueue
from ..consts import DEFAULT_BATCH_SIZE, DEFAULT_READERS
from .reader.ids import IdBatchFeeder, IdBatchQueue
from .reader.recs import CollRecsReader
from .rpt import CollExportRpt
from .writer import RecFileWriter


@dataclass
class CollExporter(CollIEBase):
  """Exports a collection to file."""

  async def export_recs(
    self,
    coll: AsyncCollection,
    file_path: Path,
    *,
    p: Callable[..., None] = print,
    readers: int = DEFAULT_READERS,
    batch_size: int = DEFAULT_BATCH_SIZE,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> CollExportRpt:
    """Exports the records of a collection to a file.

    Args:
      coll: Collection to export.
      file_path: Path to the JSONL file where to save the records.
      p: Function to use for printing the progress.
      readers: Number of concurrent readers to use.
      limit: Maximum number of records to export.
      metafilter: Filter by metadata to apply.

    Returns:
      An export report.
    """

    # (1) pre
    start = time()
    id_q, rec_q = IdBatchQueue(maxsize=15), RecBatchQueue()

    # (2) export
    async with TaskGroup() as ig, TaskGroup() as wg:
      # id batch generator
      ig.create_task(
        IdBatchFeeder(
          coll=coll,
          queue=id_q,
          batch_size=batch_size,
          limit=limit,
          metafilter=metafilter,
        ).run(),
        name="Id batch feeder",
      )

      # JSONL writer
      wt = wg.create_task(
        RecFileWriter(
          file_path=file_path,
          queue=rec_q,
        ).run(p=p),
        name="Record file writer",
      )

      # record batch generators
      async with TaskGroup() as rg:
        for i in range(readers):
          rg.create_task(
            CollRecsReader(
              coll=coll,
              queue=rec_q,
              id_queue=id_q,
            ).run(p=p),
            name=f"Coll records reader #{i + 1}",
          )

      rec_q.shutdown()  # this is closed when all the readers nothing to read

    # wait for the queues closed
    await id_q.join()
    await rec_q.join()

    # (3) return report
    return CollExportRpt(
      coll=coll.name,
      batches=wt.result()[0],
      count=wt.result()[1],
      duration=int(time() - start),
      file_path=str(file_path),
    )


def _build_coll_repr(coll: AsyncCollection) -> str:
  """Gets the configuration of a collection and builds its textual representation
  to attach in the export file.

  Args:
    coll: Collection object.

  Returns:
    Collection representation.
  """

  return (
    f'{{"name": "{coll.name}", "configuration": {json.dumps(coll.configuration_json)}}}'
  )
