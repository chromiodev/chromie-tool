from dataclasses import dataclass
from time import time

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._db import CollIEBase
from ..exp.reader import CollReader
from .rpt import CollCopyRpt


@dataclass
class CollCopier(CollIEBase):
  """Copy a collection from an instance to another."""

  async def copy_coll(
    self,
    src_coll: AsyncCollection,
    dst_coll: AsyncCollection,
    /,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> CollCopyRpt:
    """Copy a collection from an instance to another.

    Args:
      src_coll: Collection to copy.
      dst_coll: Collection where to copy.
      limit: Maximum number of records to export.
      metafilter: Filter by metadata.

    Returns:
      A copy report.
    """

    # (1) pre
    reader = CollReader()

    # (2) copy
    count, start = 0, time()

    async for batch in reader.read(
      src_coll, self.fields, self.batch_size, limit, metafilter
    ):
      await dst_coll.add(
        documents=[r["document"] for r in batch],
        metadatas=[r["metadata"] for r in batch],
        ids=[r["id"] for r in batch],
      )

      count += len(batch)

    # (3) return report
    return CollCopyRpt(
      coll=src_coll.name,
      dst_coll=dst_coll.name,
      count=count,
      duration=int(time() - start),
    )
