import json
from dataclasses import dataclass
from pathlib import Path
from time import time

from aiofiles import open
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
    file: Path,
    *,
    limit: int | None = None,
    remove: list[str] = [],
    set: dict = {},
  ) -> CollImportRpt:
    """Imports a collection from a file.

    Args:
      coll: Collection to import.
      file: File path to import.
      limit: Maximum number of records to import.
      remove: Metadata to remove in the import.
      set: Metadata to set/override in the import.

    Returns:
      An import report.
    """

    # (1) read the export file
    start = time()
    recs = []

    # load
    async with open(file, mode="r") as f:
      recs = json.loads(await f.read())["data"]

    # remove/set metafields if needed
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
    return CollImportRpt(
      coll=coll.name,
      count=count,
      duration=int(time() - start),
      file_path=str(file),
    )
