import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, override

from aiofiles import open, ospath
from chromadb.errors import NotFoundError

from chromio.client import client
from chromio.ie import Field
from chromio.ie.consts import DEFAULT_BATCH_SIZE, DEFAULT_WRITERS
from chromio.ie.imp.importer import CollImporter
from chromio.tools import Cmd
from chromio.tools.db import DbTool
from chromio.uri import parse_uri

from ._consts import EMBEDDING_FNS, SPACES


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
        "help": "path to the JSONL file to import",
        "required": True,
        "type": Path,
      },
      {
        "names": ["metafile"],
        "help": "path to the JSON metadata file to use in the import",
        "required": False,
        "type": Path,
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
        "help": f"Space: {', '.join(SPACES)}.",
        "choices": SPACES,
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
        "names": ["--batch-size", "-b"],
        "help": "size of the record batches",
        "type": int,
        "metavar": "int",
        "default": DEFAULT_BATCH_SIZE,
      },
      {
        "names": ["--limit", "-l"],
        "help": "maximum number of records to import",
        "type": int,
        "metavar": "int",
        "required": False,
      },
      {
        "names": ["--writers", "-w"],
        "help": "number of workers to use for writing the data",
        "type": int,
        "metavar": "int",
        "default": DEFAULT_WRITERS,
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
    # (1) preconditions
    # source files must exist
    if not await ospath.isfile(file := args.input):
      print(f"File '{file}' not found.", file=sys.stderr)
      exit(1)

    if (metafile := args.metafile) is not None and not await ospath.isfile(metafile):
      print(f"File '{metafile}' not found.", file=sys.stderr)
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
    batch_size, limit, writers = args.batch_size, args.limit, args.writers
    fields = [Field[args.fields[i]] for i in range(len(args.fields))]
    remove = md if (md := args.metadata_to_remove) is not None else []
    set = md if (md := args.metadata_to_set) is not None else {}
    efn, model, space = args.embedding, args.model, args.space
    progress = not args.no_progress

    # (3) get collection creating it if not exists
    cli = await client(uri, api_key)

    try:
      coll = await cli.get_collection(coll_name)
    except NotFoundError:
      # read metadata file content
      if metafile is not None:
        async with open(metafile, "r") as f:
          c = json.loads(await f.read())
      else:
        c = {"coll": {}}

      # configuration to use
      conf = c.get("configuration", {})

      if efn is not None:
        efn_conf = conf.setdefault("embedding_function", {})

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
          conf.setdefault("spann", {})["space"] = space

      # create collection
      coll = await DbTool(cli).create_coll_with_conf(coll_name, conf)

    # (4) import
    try:
      # import
      importer = CollImporter(batch_size, fields)

      rpt = await importer.import_coll(
        coll,
        file,
        limit=limit,
        writers=writers,
        remove=remove,
        set=set,
        p=print if progress else lambda *_: None,
      )

      # show report
      print(
        (
          f"{'\n' if progress else ''}"
          f"Source file: {file}\n"
          f"Destination collection: {rpt.coll}\n"
          f"Batches performed: {rpt.batches}\n"
          f"Records written: {rpt.count}\n"
          f"Duration (s): {rpt.duration}"
        )
      )
    except Exception as e:
      print(e, file=sys.stderr)
      exit(1)
