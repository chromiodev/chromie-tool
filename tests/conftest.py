import json
import os
from pathlib import Path
from typing import AsyncIterator

import pytest
from aiofiles import open
from chromadb import AsyncHttpClient, HttpClient
from chromadb.api import AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from pytest import Config, FixtureRequest
from pytest_docker.plugin import Services

from chromio.uri import default_server_host, default_server_port

# pytester plugin enabling.
pytest_plugins = "pytester"

###########
# helpers #
###########


async def __truncate_coll(coll: AsyncCollection) -> None:
  """Truncates the given collection."""

  await coll.delete(where={"director": {"$ne": "<truncate>"}})


############
# fixtures #
############

if os.getenv("GITHUB_ACTIONS") == "true":

  @pytest.fixture(scope="session")
  def server() -> tuple[str, int]:  # type: ignore
    """Connection string for the Chroma service on GitHub Actions."""

    return (default_server_host, default_server_port)
else:

  @pytest.fixture(scope="session")
  def docker_compose_project_name() -> str:
    """Docker Compose project name to use."""

    return "chromio"

  @pytest.fixture(scope="session")
  def server(docker_services: Services, docker_ip: str) -> tuple[str, int]:
    """Starts the Chroma instance for the (local) tests and returns
    its host and port.
    """

    def ping(host: str, port: int) -> bool:
      cli = HttpClient(host, port)

      try:
        cli.heartbeat()
        return True
      except Exception:
        return False

    # (1) determine service connection info
    host = docker_ip
    port = docker_services.port_for("chroma", default_server_port)

    # (2) wait for the service started
    docker_services.wait_until_responsive(
      timeout=30.0, pause=1.0, check=lambda: ping(host, port)
    )

    # (3) return URI
    return (host, port)


#############
# test data #
#############


@pytest.fixture(scope="session")
def default_batch_size() -> int:
  """Default batch size to use in the tests."""

  return 2


@pytest.fixture(scope="session")
def data_dir(pytestconfig: Config) -> Path:
  """Path to the test data directory."""

  return pytestconfig.rootpath / "tests" / "data"


@pytest.fixture(scope="module")
async def qt_records(data_dir: Path) -> list[dict]:
  """Test records (Quentin Tarantino movies) to use in the tests."""

  # (1) read the data file
  async with open(data_dir / "qt-movies.json", mode="r") as f:
    c = await f.read()

  # (2) return the records
  return json.loads(c)


@pytest.fixture(scope="module")
async def cc_records(data_dir: Path) -> list[dict]:
  """Test records (Charles Chaplin movies) to use in the tests."""

  # (1) read the data file
  async with open(data_dir / "cc-movies.json", mode="r") as f:
    c = await f.read()

  # (2) return the records
  return json.loads(c)


@pytest.fixture(scope="module")
def cc_count(cc_records: list[dict]) -> int:
  """Number of Charles Chaplin records to use in the tests."""

  return len(cc_records)


@pytest.fixture(scope="module")
async def cc_record_batches(
  cc_records: list[dict], default_batch_size: int
) -> list[list[dict]]:
  """Record batches (Charles Chaplin movies) to use in the tests."""

  return [
    cc_records[i : i + default_batch_size]
    for i in range(0, len(cc_records), default_batch_size)
  ]


@pytest.fixture(scope="module")
async def cc_export(data_dir: Path) -> str:
  """cc-export.json content to use in the tests."""

  async with open(data_dir / "cc-export.json", mode="r") as f:
    return await f.read()


@pytest.fixture(scope="module")
def records(
  request: FixtureRequest, qt_records: list[dict], cc_records: list[dict]
) -> list[dict]:
  """Records to use in the tests.
  This can be indirectly: all, qt, cc or a specific number of records.
  """

  match p := request.param if hasattr(request, "param") else "all":
    case int(p):
      return (qt_records + cc_records)[:p]
    case "qt":
      return qt_records
    case "cc":
      return cc_records
    case _:
      return qt_records + cc_records


@pytest.fixture(scope="module")
def record_batches(
  request: FixtureRequest, default_batch_size: int, records: list[dict]
) -> list[list[dict]]:
  """Indirect fixture for getting the record batches attending to given specific
  size.
  """

  # (1) args
  bs = int(request.param) if hasattr(request, "param") else default_batch_size

  # (2) return
  return [records[i : i + bs] for i in range(0, len(records), bs)]


@pytest.fixture(scope="module")
async def record(qt_records: list[dict]) -> dict:
  """A record to use in the tests."""

  return qt_records[0]


@pytest.fixture(scope="module")
async def new_record(cc_records: list[dict]) -> dict:
  """A new record to use in the tests."""

  return cc_records[0]


######
# DB #
######


@pytest.fixture(scope="module")
async def db(server: tuple[str, int]) -> AsyncClientAPI:
  """Database to use for performing the assessments."""

  return await AsyncHttpClient(host=server[0], port=server[1])


@pytest.fixture(scope="function")
async def coll(db: AsyncClientAPI) -> AsyncCollection:
  """Collection to use in the tests."""

  return await db.create_collection("pytest", get_or_create=True)


@pytest.fixture(scope="module")
async def coll2(db: AsyncClientAPI) -> AsyncCollection:
  """Second collection to use in some tests such as, for example,
  these functional.
  """

  return await db.create_collection("pytest2", get_or_create=True)


@pytest.fixture(scope="function")
async def arrange_coll(
  coll: AsyncCollection, qt_records: list[dict]
) -> AsyncIterator[None]:
  """Arranges the collection to use in the tests."""

  # (1) populate the collection
  await coll.add(
    ids=[r["id"] for r in qt_records],
    metadatas=[r["metadata"] for r in qt_records],
    documents=[r["document"] for r in qt_records],
  )

  # (2) return
  yield

  # (3) cleanup
  await __truncate_coll(coll)


@pytest.fixture(scope="function")
async def truncate_coll(coll: AsyncCollection) -> AsyncIterator[None]:
  """Truncates the collection to use in the tests in the beginning and in the end."""

  yield
  await __truncate_coll(coll)


@pytest.fixture(scope="module")
async def arrange_coll2(coll2: AsyncCollection, cc_records: list[dict]) -> None:
  """Arranges the 2nd collection to use in the tests."""

  for r in cc_records:
    await coll2.add(ids=r["id"], metadatas=r["metadata"], documents=r["document"])
