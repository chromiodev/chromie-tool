import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.filter import MetaFilterParser
from chromio.ie import Field
from chromio.ie.consts import DEFAULT_BATCH_SIZE
from chromio.ie.cp.copier import CollCopier
from chromio.tools import Cmd
from chromio.uri import parse_uri


@dataclass(frozen=True)
class CpCmd(Cmd):
  """Copy one collection."""

  # @override
  name: str = "cp"

  # @override
  help: str = "Copy a collection."

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
        "names": ["dst"],
        "help": "destination URI",
        "required": True,
      },
      {
        "names": ["--src-key", "-k"],
        "help": "API key to use, if needed, for connecting to source server",
        "metavar": "token",
        "default": os.getenv("CHROMA_API_KEY"),
        "required": False,
      },
      {
        "names": ["--dst-key", "-K"],
        "help": "API key to use, if needed, for connecting to destination server",
        "metavar": "token",
        "default": os.getenv("CHROMA_API_KEY"),
        "required": False,
      },
      {
        "names": ["--fields", "-F"],
        "help": "fields to copy",
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
        "help": "maximum number of records to copy",
        "type": int,
        "metavar": "int",
        "required": False,
      },
      {
        "names": ["--metafilter", "-f"],
        "help": "metadata filter for selecting the records to copy",
        "metavar": "expr",
        "required": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) precondition: API key if needed
    src_api_key, dst_api_key = None, None

    if (src_uri := parse_uri(args.src)).schema == "cloud" and not (
      src_api_key := args.src_key
    ):
      print("Expected API key for source Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    if (dst_uri := parse_uri(args.dst)).schema == "cloud" and not (
      dst_api_key := args.dst_key
    ):
      print("Expected API key for destination Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    # (2) precondition: collection expected in the URI
    if (src_coll_name := src_uri.coll) is None:
      print(f"Expected collection in the source URI: '{src_uri}'.", file=sys.stderr)
      exit(1)

    if (dst_coll_name := dst_uri.coll) is None:
      print(f"Expected collection in the destination URI: '{dst_uri}'.", file=sys.stderr)
      exit(1)

    # (3) args
    batch_size, limit = args.batch, args.limit
    fields = [Field[args.fields[i]] for i in range(len(args.fields))]
    metafilter = MetaFilterParser().parse(exp) if (exp := args.metafilter) else None

    # (4) create clients
    src_cli = await client(src_uri, src_api_key)
    src_coll = await src_cli.get_collection(src_coll_name)

    dst_cli = await client(dst_uri, dst_api_key)
    dst_coll = await dst_cli.get_or_create_collection(dst_coll_name)

    # (5) copy
    copier = CollCopier(batch_size, fields)
    rpt = await copier.copy_coll(src_coll, dst_coll, limit=limit, metafilter=metafilter)

    # (6) show report
    print(
      (
        f"Source collection: {rpt.coll}\n"
        f"Destination collection: {rpt.dst_coll}\n"
        f"Count: {rpt.count}\n"
        f"Duration (s): {rpt.duration}\n"
      )
    )
