import pytest
from chromadb.api import AsyncClientAPI
from pytest_mock import MockerFixture

from chromio.errors import CollAlreadyExistsError, CollNotFoundError
from chromio.tools.db import DbTool


@pytest.fixture(scope="function")
def tool(mocker: MockerFixture) -> DbTool:
  """DB tool to use in the tests."""

  return DbTool(db=mocker.AsyncMock(spec=AsyncClientAPI))


async def test_get_coll_conf_existing(mocker: MockerFixture, tool: DbTool) -> None:
  """Check that get_coll_conf() returns the configuration of an existing collection."""

  # (1) arrange
  tool.db.get_collection = get_collection = mocker.AsyncMock(
    return_value=(coll := mocker.Mock())
  )
  type(coll).configuration_json = mocker.PropertyMock(
    return_value={
      "hnsw": None,
      "spann": {
        "search_nprobe": 64,
        "write_nprobe": 32,
        "space": "cosine",
        "ef_construction": 200,
        "ef_search": 200,
        "max_neighbors": 64,
        "reassign_neighbor_count": 64,
        "split_threshold": 50,
        "merge_threshold": 25,
      },
      "embedding_function": {
        "type": "known",
        "name": "sentence_transformer",
        "config": {
          "device": "cpu",
          "kwargs": {},
          "model_name": "all-MiniLM-L6-v2",
          "normalize_embeddings": False,
        },
      },
    }
  )

  # (2) act
  out = await tool.get_coll_conf("pytest")

  # (3) assessment
  assert isinstance(out, dict)
  assert out["spann"]["space"] == "cosine"
  assert get_collection.await_count == 1


async def test_get_coll_conf_unexisting(mocker: MockerFixture, tool: DbTool) -> None:
  """Check that get_coll_conf() raises error when collection not existing."""

  # (1) arrange
  tool.db.get_collection = mocker.AsyncMock(side_effect=Exception())

  # (2) act and assessment
  with pytest.raises(CollNotFoundError, match="'pytest' not found"):
    await tool.get_coll_conf("pytest")


async def test_create_coll_new(mocker: MockerFixture, tool: DbTool) -> None:
  """Check that create_coll() creates a new collection when not existing."""

  # (1) arrange
  tool.db.get_collection = get_collection = mocker.AsyncMock(side_effect=ValueError())
  tool.db.create_collection = create_collection = mocker.AsyncMock(return_value=None)

  # (2) act
  out = await tool.create_coll("pytest", efn="Default", space="l2")

  # (3) assessment
  assert isinstance(out, dict)
  assert out["embedding_function"] is not None
  assert out["hnsw"]["space"] == "l2"

  assert get_collection.await_count == 1
  assert create_collection.await_count == 1


async def test_create_coll_existing(mocker: MockerFixture, tool: DbTool) -> None:
  """Check that create_coll() raises error if collection already existing."""

  # (1) arrange
  tool.db.get_collection = get_collection = mocker.AsyncMock(return_value={})

  # (2) act
  with pytest.raises(CollAlreadyExistsError, match="'pytest' already exists"):
    await tool.create_coll("pytest")

  # (3) assessment
  assert get_collection.await_count == 1
