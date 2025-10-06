from dataclasses import dataclass
from typing import Any, override

from chromio.tools import Cmd
from chromio.uri import parse_uri


@dataclass(frozen=True)
class UriCmd(Cmd):
  """Decompose a URI and print its segments."""

  # @override
  name: str = "uri"

  # @override
  help: str = "Show the segments of a URI."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["uri"],
        "help": "URI to parse",
        "required": True,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) decompose URI
    uri = parse_uri(args.uri)

    # (2) print segments
    print("Schema:", uri.schema)
    print("Host:", uri.host)
    print("Port:", uri.port)
    print("Tenant:", uri.tenant)
    print("Database:", uri.db)
