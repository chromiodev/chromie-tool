import asyncio
from asyncio import QueueShutDown
from dataclasses import dataclass
from typing import Any, Callable, cast

from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.api.types import Include

from ...._core import Rec
from ...._reader import RecBatchReader
from ....consts import DEFAULT_FIELDS
from ....field import Field
from ..ids import IdBatchQueue


@dataclass
class CollRecsReader(RecBatchReader):
  """A worker for reading the records of a collection, putting them into an
  asynchronous queue.

  This component doesn't need to know the limit to export
  """

  id_queue: IdBatchQueue
  """Queue where the id batches are saved."""

  coll: AsyncCollection
  """Collection to export/read."""

  fields = DEFAULT_FIELDS
  """Fields to export."""

  async def run(self, p: Callable[..., None]) -> None:
    """Runs the reader."""

    # (1) prepare working context
    name: str = cast(Any, asyncio.current_task()).get_name()
    coll, fields, id_q, rec_q = self.coll, self.fields, self.id_queue, self.queue
    include = cast(Include, [str(fld) for fld in fields if fld != Field.id])

    # (2) read the records and add them to queue
    try:
      while True:
        # read records from their ids
        ids = await id_q.get()
        id_q.task_done()

        p(f"{name}: reading record batch from collection...")

        if (size := len((res := await coll.get(ids=ids, include=include))["ids"])) <= 0:
          continue

        # prepare batch to yield
        batch = []

        for i in range(size):
          rec: Rec = {"id": res["ids"][i]}

          if Field.meta in fields:
            rec["metadata"] = cast(list[dict], res["metadatas"])[i]

          if Field.doc in fields:
            rec["document"] = cast(list[str], res["documents"])[i]

          batch.append(rec)

        # add to queue
        await rec_q.put(batch)
    except QueueShutDown:
      pass
