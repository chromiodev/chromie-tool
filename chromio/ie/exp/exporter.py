import json
from dataclasses import dataclass
from pathlib import Path
from time import time

from aiofiles import open
from chromadb.api.models.AsyncCollection import AsyncCollection

from .._db import CollIEBase
from . import jsonl
from .reader import CollReader
from .rpt import CollExportRpt


@dataclass
class CollExporter(CollIEBase):
  """Exports collections to files."""

  async def export_coll(
    self,
    coll: AsyncCollection,
    file: Path,
    *,
    v: str,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> CollExportRpt:
    """Exports a collection to a file.

    Args:
      coll: Collection to export.
      file: File path where to save the export.
      v: Chroma instance version.
      limit: Maximum number of records to export.
      metafilter: Filter by metadata.

    Returns:
      An export report.
    """

    # (1) pre
    reader = CollReader()

    # (2) export
    count, start = 0, time()

    async with open(file, mode="w") as f:
      # start
      await f.write('{\n  "version": "1.0",\n')

      # metadata
      await f.writelines(
        [
          '  "metadata": {\n',
          f'    "chroma": {{"version": "{v}"}},\n',
          f'    "coll": {_build_coll_repr(coll)}\n',
          "  },\n",
        ]
      )

      # data
      await f.write('  "data": [\n')

      async for batch in reader.read(
        coll, self.fields, self.batch_size, limit, metafilter
      ):
        await f.writelines(
          [
            ",\n" if count > 0 else "",
            jsonl.dumps(batch, indent=4, sep=",\n"),
            "",
          ]
        )
        count += len(batch)

      await f.write("\n  ]\n")

      # end
      await f.write("}\n")

    # (3) return report
    return CollExportRpt(
      coll=coll.name,
      count=count,
      duration=int(time() - start),
      file_path=str(file),
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
