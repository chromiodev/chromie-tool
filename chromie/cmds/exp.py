import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.filter.metadata import MetafilterParser
from chromio.ie import Field
from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_READERS
from chromio.ie.exp import CollExporter
from chromio.tools import Cmd
from chromio.uri import parse_uri


@dataclass(frozen=True)
class ExpCmd(Cmd):
  # @override
  name: str = "exp"

  # @override
  help: str = "Export a collection."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["src"],
        "help": "source URI",
        "required": True,
      },
      {
        "names": ["out"],
        "help": "file path where to export",
        "required": True,
      },
      {
        "names": ["--key", "-k"],
        "help": "API key to use, if needed, for connecting to server",
        "metavar": "token",
        "default": os.getenv("CHROMA_API_KEY"),
        "required": False,
      },
      {
        "names": ["--fields", "-F"],
        "help": "fields to export",
        "action": "store",
        "nargs": "*",
        "choices": ["meta", "doc", "embedding"],
        "default": ["meta", "doc"],
      },
      {
        "names": ["--batch", "-b"],
        "help": "batch size",
        "type": int,
        "metavar": "int",
        "required": False,
        "default": DEFAULT_BATCH_SIZE,
      },
      {
        "names": ["--limit", "-l"],
        "help": "maximum number of records to export",
        "type": int,
        "metavar": "int",
        "required": False,
      },
      {
        "names": ["--metafilter", "-f"],
        "help": "metadata filter for selecting the records to export",
        "metavar": "expr",
        "required": False,
      },
      {
        "names": ["--readers", "-r"],
        "help": "number of readers to use for reading the records",
        "type": int,
        "metavar": "int",
        "default": DEFAULT_READERS,
      },
      {
        "names": ["--no-progress", "-P"],
        "help": "do not print the progress",
        "action": "store_true",
        "default": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) precondition: API key if needed
    api_key = None

    if (uri := parse_uri(args.src)).schema == "cloud" and not (api_key := args.key):
      print("Expected API key for Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    # (2) precondition: collection expected in the URI
    if (coll_name := uri.coll) is None:
      print(f"Expected collection in the URI: '{uri}'.", file=sys.stderr)
      exit(1)

    # (3) args
    file = args.out
    batch_size, limit, readers = args.batch, args.limit, args.readers
    fields = [Field[args.fields[i]] for i in range(len(args.fields))]
    progress = not args.no_progress
    metafilter = (
      MetafilterParser().parse(exp).to_chroma() if (exp := args.metafilter) else None
    )

    # (4) create client
    cli = await client(uri, api_key)
    coll = await cli.get_collection(coll_name)

    # (5) export
    exporter = CollExporter(batch_size, fields)
    rpt = await exporter.export_recs(
      coll,
      file,
      readers=readers,
      batch_size=batch_size,
      limit=limit,
      metafilter=metafilter,
      p=print if progress else lambda *_: None,
    )

    # (6) show report
    print(
      (
        f"Collection exported: {rpt.coll}\n"
        f"Batches performed: {rpt.batches}\n"
        f"Records exported: {rpt.count}\n"
        f"Duration (s): {rpt.duration}\n"
        f"Data export file: {rpt.file_path}"
      )
    )
