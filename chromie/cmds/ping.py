import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.tools import Cmd
from chromio.uri import ChromioUri, parse_uri


@dataclass(frozen=True)
class PingCmd(Cmd):
  """Performs a ping to a database instance."""

  # @override
  name: str = "ping"

  # @override
  help: str = "Ping a database or a collection."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["uri"],
        "help": "URI to ping",
        "required": True,
      },
      {
        "names": ["--key", "-k"],
        "help": "API key to use, if needed, for connecting to server",
        "metavar": "token",
        "default": os.getenv("CHROMA_API_KEY"),
        "required": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) decompose the URI
    uri = parse_uri(args.uri)

    # (2) ping
    match uri.schema:
      case "server":
        await _ping(uri)

      case "cloud":
        await _ping(uri, args.key)


async def _ping(uri: ChromioUri, api_key: str | None = None) -> None:
  """Pings a database or a collection, attending to the URI.

  Args:
    uri: Cloud URI to ping.
    api_key: API key to use.
  """

  # (1) create cloud client
  cli = await client(uri, api_key)

  # (2) ping
  await cli.heartbeat()
  print("Ping database: ok")

  if (coll_name := uri.coll) is not None:
    try:
      await cli.get_collection(coll_name)
      print("Ping collection: ok")
    except Exception:
      print("Ping collection failed!", file=sys.stderr)
      exit(1)
