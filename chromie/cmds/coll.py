import os
import sys
from dataclasses import dataclass
from typing import Any, override

from chromio.client import client
from chromio.errors import CollAlreadyExistsError, CollNotFoundError
from chromio.tools import Cmd
from chromio.tools.db import DbTool
from chromio.uri import parse_uri

EMBEDDING_FNS = ("Default", "SentenceTransformer")
HNSW_SPACES = ("cosine", "ip", "l2")


@dataclass(frozen=True)
class CollCmd(Cmd):
  # @override
  name: str = "coll"

  # @override
  help: str = "Create or show configuration on a collection."

  @property
  @override
  def args(self) -> list[dict]:
    return [
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
        "names": ["--info", "-i"],
        "help": "show configuration of an existing collection",
        "action": "store_true",
      },
      {
        "names": ["--embedding", "--efn", "-e"],
        "help": "Embedding function to use.",
        "choices": EMBEDDING_FNS,
      },
      {
        "names": ["--model", "-m"],
        "help": (
          "Model to use, only used if embedding set and not Default. "
          "For example, for SentenceTransformer: "
          "all-MiniLM-L6-v2, all-MiniLM-L12-v2 or paraphrase-multilingual-MiniLM-L12-v2.all-MiniLM-L12-v2"
        ),
        "default": "all-MiniLM-L6-v2",
      },
      {
        "names": ["--space"],
        "help": "HNSW space.",
        "choices": HNSW_SPACES,
        "default": HNSW_SPACES[0],
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) args
    api_key, efn, model, space = (
      args.key,
      args.embedding,
      args.model,
      args.space,
    )

    if (uri := parse_uri(args.dst)).schema == "cloud" and not (api_key := args.key):
      print("Expected API key for Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    if uri.coll is None:
      print("Expected collection name.", file=sys.stderr)
      exit(1)

    # (2) create db tool to use
    try:
      db = DbTool(await client(uri, api_key))
    except Exception as e:
      print(f"Server or database not found: '{e}'.", file=sys.stderr)
      exit(1)

    # (3) perform operation
    name = uri.coll

    if args.info:
      try:
        print(await db.get_coll_conf(name))
      except CollNotFoundError:
        print(f"Collection '{name}' not found.", file=sys.stderr)
        exit(1)
    else:
      try:
        conf = await db.create_coll(name, efn=efn, model=model, space=space)
        print(f"Configuration used:\n{conf}")
      except CollAlreadyExistsError:
        print(f"Collection '{name}' already exists.", file=sys.stderr)
        exit(1)
