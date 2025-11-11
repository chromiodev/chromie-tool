from dataclasses import dataclass
from typing import Literal, Self

from chromadb.config import DEFAULT_DATABASE, DEFAULT_TENANT

default_server_host = "localhost"
"""Default host for server URIs."""

default_server_port = 8000
"""Default port for server URIs."""

default_cloud_host = "api.trychroma.com"
"""Default host for cloud URIs."""

default_cloud_port = 8000
"""Default port for cloud URIs."""

default_tenant = DEFAULT_TENANT
"""Default tenant name."""

default_database = DEFAULT_DATABASE
"""Default database name."""

type UriSchema = Literal["path", "server", "cloud"]
"""The type of URI."""


@dataclass
class ChromioUri:
  """A Chromio URI to a DB instance."""

  schema: UriSchema
  """URI type."""

  path: str | None = None
  """Persistent directory. Only used with path."""

  host: str | None = None
  """Server host. Only used with server and cloud."""

  port: int | None = None
  """Server port. Only used with server and cloud."""

  tenant: str | None = None
  """Tenant. Only used with server and cloud."""

  db: str | None = None
  """Database name. Only used with server and cloud."""

  coll: str | None = None
  """Collection name."""

  @classmethod
  def server(
    cls,
    *,
    host=default_server_host,
    port=default_server_port,
    tenant=default_tenant,
    db=default_database,
    coll=None,
  ) -> Self:
    return cls(schema="server", host=host, port=port, tenant=tenant, db=db, coll=coll)

  @classmethod
  def cloud(cls) -> Self:
    return cls(schema="cloud", host=default_cloud_host, port=default_cloud_port)
