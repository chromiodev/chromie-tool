import json
from dataclasses import dataclass
from pathlib import Path
from time import time

from aiofiles import open
from chromadb.api.models.AsyncCollection import AsyncCollection

from chromio.ie.imp.writer import CollWriter

from .._db import CollIEBase
from .rpt import CollImportRpt


@dataclass
class CollImporter(CollIEBase):
  """Imports a collection from file."""

  async def import_coll(
    self,
    coll: AsyncCollection,
    file: Path,
    /,
    limit: int | None = None,
    remove: list[str] = [],
  ) -> CollImportRpt:
    """Imports a collection from a file.

    Args:
      coll: Collection to import.
      file: File path to import.
      limit: Maximum number of records to import.
      remove: Metafields to remove in the import.

    Returns:
      An import report.
    """

    # (1) read the export file
    start = time()
    recs = []

    # load
    async with open(file, mode="r") as f:
      recs = json.loads(await f.read())["data"]

    # remove metafields when needed
    if len(remove) > 0:
      recs = [
        {
          **rec,
          "metadata": {
            key: val for key, val in rec["metadata"].items() if key not in remove
          },
        }
        for rec in recs
      ]

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
