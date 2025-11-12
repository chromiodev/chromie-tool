from dataclasses import dataclass
from time import time
from typing import Any

from chromadb.api.models.AsyncCollection import AsyncCollection

from .._db import CollIEBase
from .rpt import CollImportRpt
from .writer import CollWriter


@dataclass
class CollImporter(CollIEBase):
  """Imports a collection from file."""

  async def import_coll(
    self,
    coll: AsyncCollection,
    recs: list[dict[str, Any]],
    *,
    limit: int | None = None,
    remove: list[str] = [],
    set: dict = {},
  ) -> CollImportRpt:
    """Imports the given records in a collection.

    Args:
      coll: Collection to import.
      recs: Records to import.
      limit: Maximum number of records to import.
      remove: Metadata to remove in the import.
      set: Metadata to set/override in the import.

    Returns:
      An import report.
    """

    start = time()

    # (1) remove/set metafields if needed
    if len(remove) > 0 or len(set) > 0:
      for rec in recs:
        md = rec["metadata"]

        for key in remove:
          del md[key]

        for key, val in set.items():
          md[key] = val

    # (2) write
    count = await CollWriter().write(
      recs, coll, fields=self.fields, limit=limit, batch_size=self.batch_size
    )

    # (3) return report
    return CollImportRpt(coll=coll.name, count=count, duration=int(time() - start))
