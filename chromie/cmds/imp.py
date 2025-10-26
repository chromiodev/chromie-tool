import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.ie import Field
from chromio.ie.consts import DEFAULT_BATCH_SIZE
from chromio.ie.imp.importer import CollImporter
from chromio.tools import Cmd
from chromio.uri import parse_uri


@dataclass(frozen=True)
class ImpCmd(Cmd):
  """Import one collection from a file."""

  # @override
  name: str = "imp"

  # @override
  help: str = "Import a collection from a file."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["input"],
        "help": "file path to import",
        "required": True,
      },
      {
        "names": ["dst"],
        "help": "destination URI",
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
        "help": "fields to import",
        "action": "store",
        "nargs": "*",
        "choices": ["meta", "doc", "embedding"],
        "default": ["meta", "doc"],
      },
      {
        "names": ["--metadata-to-remove", "-M"],
        "help": "Metadata to remove (separator: ',')",
        "metavar": "fld1,fld2,fld3...",
        "type": lambda arg: arg.split(","),
      },
      {
        "names": ["--metadata-to-set", "-m"],
        "help": "Metadata to set/overwrite (separator: ',')",
        "metavar": "f1:v1,f2:v2,f3:v3...",
        "type": lambda arg: {(i := kv.split(":"))[0]: i[1] for kv in arg.split(",")},
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
        "help": "maximum number of records to import",
        "type": int,
        "metavar": "int",
        "required": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) precondition: API key if needed
    api_key = None

    if (uri := parse_uri(args.dst)).schema == "cloud" and not (api_key := args.key):
      print("Expected API key for Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    # (2) precondition: collection expected in the URI
    if (coll_name := uri.coll) is None:
      print(f"Expected collection in the URI: '{uri}'.", file=sys.stderr)
      exit(1)

    # (3) args
    file = args.input
    batch_size, limit = args.batch, args.limit
    fields = [Field[args.fields[i]] for i in range(len(args.fields))]
    remove = md if (md := args.metadata_to_remove) is not None else []
    set = md if (md := args.metadata_to_set) is not None else {}

    # (4) create client
    cli = await client(uri, api_key)
    coll = await cli.create_collection(coll_name, get_or_create=True)

    # (5) import
    importer = CollImporter(batch_size, fields)
    rpt = await importer.import_coll(coll, file, limit=limit, remove=remove, set=set)

    # (6) show report
    print(
      (
        f"Collection: {rpt.coll}\n"
        f"Count: {rpt.count}\n"
        f"Duration (s): {rpt.duration}\n"
        f"File: {rpt.file_path}"
      )
    )
