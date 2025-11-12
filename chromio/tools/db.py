from dataclasses import dataclass
from typing import Any, Literal, cast

import chromadb.utils.embedding_functions as emb
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.errors import ChromaError

from ..errors import CollAlreadyExistsError, CollNotFoundError

type _Space = Literal["cosine", "ip", "l2"]


@dataclass
class DbTool:
  """Component for performing utility tasks on Chroma databases
  such as, for example, creating collections.
  """

  db: AsyncClientAPI
  """DB object to use for running the operations."""

  async def create_coll_with_conf(
    self,
    name: str,
    conf: dict[str, Any],
  ) -> AsyncCollection:
    """Creates a collection from a configuration object returned by Chroma.

    Args:
      name: Collection name.
      conf: Configuration.

    Returns:
      Collection object for this created.

    Raises:
      CollAlreadyExistsError: if the collection already exists.
      ValueError: if the embedding function is not supported.
    """

    # (1) determine configuration
    match n := (aux := conf.get("embedding_function", {})).get("name", "default"):
      case "default":
        efn = emb.DefaultEmbeddingFunction()
      case "sentence_transformer":
        efn = emb.SentenceTransformerEmbeddingFunction(
          **{k: v for k, v in aux.get("config", {}).items() if k != "kwargs"}
        )
      case _:
        raise ValueError(f"Embedding function '{n}' not supported.")

    if (hnsw := conf.get("hnsw")) is None:
      hnsw = (
        None
        if (space := conf.get("spann", {}).get("space")) is None
        else {"space": space}
      )

    # (2) create collection if not exists
    try:
      return await self.db.create_collection(
        name,
        configuration=({"embedding_function": efn, "hnsw": hnsw}),  # type: ignore
      )
    except ChromaError as e:
      if "already exists" in str(e):
        raise CollAlreadyExistsError(name)

      raise  # pragma: no cover

  async def create_coll(
    self,
    name: str,
    *,
    emb_name: str | None = None,
    model: str = "all-MiniLM-L6-v2",
    space: _Space | None = None,
  ) -> dict[str, Any]:
    """Creates a collection.

    Args:
      name: Collection name to create.
      efn_name: Embedding function to set as default in the new collection.
      model: Model name to use when needed for the embedding function.
      space: HNSW space to set.

    Returns:
      The configuration used in the creation.

    Raises:
      CollAlreadyExistsError: if the collection already exists.
    """

    # (1) arrange
    db = self.db

    # (2) determine embedding function to use
    match emb_name:
      case None:
        efn = None
      case "default":
        efn = emb.DefaultEmbeddingFunction()
      case "sentence_transformer" | "st":
        efn = emb.SentenceTransformerEmbeddingFunction(model)
      case _:  # pragma: no cover
        raise ValueError(f"Embedding function '{emb_name}' not supported.")

    # (2) create collection if not exists
    try:
      await db.create_collection(
        name,
        configuration=(
          conf := {
            "embedding_function": efn,
            "hnsw": None if (space := space) is None else {"space": space},
          }
        ),
      )

      return cast(dict[str, Any], conf)
    except ChromaError as e:
      if "already exists" in str(e):
        raise CollAlreadyExistsError(name)

      raise  # pragma: no cover

  async def get_coll_conf(self, name: str) -> dict[str, Any]:
    """Returns the configuration related to an existing collection.

    Args:
      name: Collection name to query.

    Returns:
      The collection information.

    Raises:
      CollNotFoundError: if the collection is not found in the database.
    """

    try:
      return (await self.db.get_collection(name)).configuration_json
    except Exception:
      raise CollNotFoundError(name)

  async def list_colls(self, *, count=False) -> list[dict[str, Any]]:
    """Returns the collections.

    Args:
      count: Must the counts be returned.

    Returns:
      The collections with its info.
    """

    db = self.db

    # (1) get collections
    colls = []

    for coll in await db.list_collections():
      info: dict[str, Any] = {"name": coll.name}

      if count:
        info["count"] = await coll.count()

      colls.append(info)

    # (2) return info
    return colls
