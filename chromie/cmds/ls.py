import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.tools import Cmd
from chromio.uri import parse_uri


@dataclass(frozen=True)
class LsCmd(Cmd):
  """List the collections from a database."""

  # @override
  name: str = "ls"

  # @override
  help: str = "List DB collections."

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
        "names": ["--key", "-k"],
        "help": "API key to use, if needed, for connecting to server",
        "metavar": "token",
        "default": os.getenv("CHROMA_API_KEY"),
        "required": False,
      },
      {
        "names": ["--count", "-c"],
        "help": "Show the number of records",
        "action": "store_true",
        "default": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) args
    api_key, count = None, args.count

    if (uri := parse_uri(args.src)).schema == "cloud" and not (api_key := args.key):
      print("Expected API key for Chroma Cloud connection.")
      exit(1)

    # (2) create client
    try:
      cli = await client(uri, api_key)
    except Exception as e:
      print(f"Server or database not found: '{e}'.", file=sys.stderr)
      exit(1)

    # (3) print
    for coll in await cli.list_collections():
      print(coll.name, end="")

      if count:
        print(":", await coll.count())
      else:
        print()
