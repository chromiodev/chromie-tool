import os
import sys
from dataclasses import dataclass
from typing import Any, override

import chromadb.utils.embedding_functions as emb

from chromio.client import client
from chromio.tools import Cmd
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
        "names": ["--embedding", "-e"],
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
    api_key, emb_fn, model, space = (
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

    # (2) create client
    try:
      cli = await client(uri, api_key)
    except Exception as e:
      print(f"Server or database not found: '{e}'.", file=sys.stderr)
      exit(1)

    # (3) perform operation
    name = uri.coll

    if args.info:
      coll = await cli.get_collection(name)
      print(coll.configuration_json)
    else:
      try:
        await cli.get_collection(name)
        print(f"Collection '{name}' already exists.", file=sys.stderr)
        exit(1)
      except Exception:
        await cli.create_collection(
          name,
          configuration=(
            conf := {
              "embedding_function": (
                emb.DefaultEmbeddingFunction()
                if emb_fn is None or emb_fn == "Default"
                else emb.SentenceTransformerEmbeddingFunction(model)
              ),
              "hnsw": None if (space := space) is None else {"space": space},
            }
          ),
        )

        print(f"Configuration used:\n{conf}")
