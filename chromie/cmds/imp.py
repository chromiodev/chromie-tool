import json
import os
import sys
from dataclasses import dataclass
from typing import Any, override

from aiofiles import open, ospath
from chromadb.errors import NotFoundError

from chromio.client import client
from chromio.ie import Field
from chromio.ie.consts import DEFAULT_BATCH_SIZE
from chromio.ie.imp.importer import CollImporter
from chromio.tools import Cmd
from chromio.tools.db import DbTool
from chromio.uri import parse_uri

from ._consts import EMBEDDING_FNS, HNSW_SPACES


@dataclass(frozen=True)
class ImpCmd(Cmd):
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
        "names": ["--embedding", "--efn", "-e"],
        "metavar": "name",
        "help": f"Embedding function to set if collection to create: {', '.join(EMBEDDING_FNS)}.",
        "choices": EMBEDDING_FNS,
      },
      {
        "names": ["--model", "-o"],
        "metavar": "name",
        "help": (
          "Model to use. Only used if embedding is sentence_transformer. "
          "Examples: "
          "all-MiniLM-L6-v2, all-MiniLM-L12-v2, "
          "paraphrase-multilingual-MiniLM-L12-v2 or "
          "paraphrase-multilingual-mpnet-base-v2."
        ),
        "default": "all-MiniLM-L6-v2",
      },
      {
        "names": ["--space"],
        "help": f"HNSW space: {', '.join(HNSW_SPACES)}.",
        "choices": HNSW_SPACES,
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
    # (1) preconditions
    # source file must exist
    if not await ospath.isfile(file := args.input):
      print(f"File '{file}' not found.", file=sys.stderr)
      exit(1)

    # API key if needed
    api_key = None

    if (uri := parse_uri(args.dst)).schema == "cloud" and not (api_key := args.key):
      print("Expected API key for Chroma Cloud connection.", file=sys.stderr)
      exit(1)

    # collection expected in the URI
    if (coll_name := uri.coll) is None:
      print(f"Expected collection in the URI: '{uri}'.", file=sys.stderr)
      exit(1)

    # (2) args
    batch_size, limit = args.batch, args.limit
    fields = [Field[args.fields[i]] for i in range(len(args.fields))]
    remove = md if (md := args.metadata_to_remove) is not None else []
    set = md if (md := args.metadata_to_set) is not None else {}
    efn, model, space = args.embedding, args.model, args.space

    # (3) read file
    async with open(file, "r") as f:
      c = json.loads(await f.read())

    # (4) get collection creating it if not exists
    cli = await client(uri, api_key)

    try:
      coll = await cli.get_collection(coll_name)
    except NotFoundError:
      # configuratioon to use
      conf = c["metadata"]["coll"].get("configuration", {})

      if efn is not None:
        conf["embedding_function"] = efn_conf = conf.get("embedding_function", {})

        match efn:
          case "default":
            efn_conf["name"] = "default"
          case "sentence_transformer":
            efn_conf["name"] = "sentence_transformer"
            efn_conf["config"] = {
              "device": "cpu",
              "kwargs": {},
              "model_name": model,
              "normalize_embeddings": False,
            }

        if space is not None:
          (spann_conf := conf.get("spann", {}))["space"] = space
          conf["spann"] = spann_conf

      # create collection
      coll = await DbTool(cli).create_coll_with_conf(coll_name, conf)

    # (5) import
    importer = CollImporter(batch_size, fields)
    rpt = await importer.import_coll(coll, c["data"], limit=limit, remove=remove, set=set)

    # (6) show report
    print(
      (
        f"Collection: {rpt.coll}\n"
        f"Count: {rpt.count}\n"
        f"Duration (s): {rpt.duration}\n"
        f"File: {file}"
      )
    )
