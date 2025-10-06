from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any, cast

from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.api.types import Include

from ..consts import DEFAULT_BATCH_SIZE, DEFAULT_FIELDS
from ..field import Field


@dataclass
class CollReader:
  """A component for reading records from collections."""

  async def read(
    self,
    coll: AsyncCollection,
    /,
    fields=DEFAULT_FIELDS,
    batch_size=DEFAULT_BATCH_SIZE,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> AsyncGenerator[list[dict]]:
    """Reads data from a collection.

    Args:
      coll: Collection to read.
      fields: Fields to read.
      batch_size: Number of records to read in every batch.
      limit: Maximum number of records to read. If None, all of them.
      metafilter: Record filter by metadata.

    Returns:
      The record batches.
    """

    # (1) pre
    include = cast(Include, [str(fld) for fld in fields if fld != Field.id])

    # (2) read
    start, ended = 0, False

    while not ended:
      # set offset and batch size (the last one can be less than this passed)
      offset = start * batch_size

      if limit is not None and offset + batch_size >= limit:
        ended, batch_size = True, limit - offset

      # read next batch, exiting if no more records
      if (
        size := len(
          (
            res := await coll.get(
              include=include, where=metafilter, offset=offset, limit=batch_size
            )
          )["ids"]
        )
      ) == 0:
        break

      start += 1

      # prepare batch to yield
      batch = []

      for i in range(size):
        rec: dict[str, Any] = {"id": res["ids"][i]}

        if Field.meta in fields:
          rec["metadata"] = cast(list[dict], res["metadatas"])[i]

        if Field.doc in fields:
          rec["document"] = cast(list[str], res["documents"])[i]

        batch.append(rec)

      # yield batch
      yield batch
