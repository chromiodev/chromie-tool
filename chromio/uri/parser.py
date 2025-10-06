import os
import re

from .uri import (
  ChromioUri,
  default_cloud_host,
  default_cloud_port,
  default_database,
  default_server_host,
  default_server_port,
  default_tenant,
)


def parse_uri(uri: str) -> ChromioUri:
  """Validate a given URI.
  Uses the following env variables if needed: CHROMA_HOST, CHROMA_PORT,
  CHROMA_TENANT and CHROMA_DATABASE.

  Args:
    uri: URI to validate.

  Raises:
    ValueError: if the URI is not valid.
  """

  if uri.startswith("path://"):
    return ChromioUri(schema="path", path=uri[7:])
  elif uri.startswith("server://"):
    return __parse_server_uri(uri)
  elif uri.startswith("cloud://"):
    return __parse_cloud_uri(uri)
  else:
    raise ValueError(f"Invalid URI schema: '{uri}'.")


def __parse_server_uri(uri: str) -> ChromioUri:
  """Parses a server URI. It can be one of the following:

  - server:////: CHROMA_HOST, CHROMA_PORT, CHROMA_TENANT and CHROMA_DATABASE
  - server://///coll: CHROMA_HOST, CHROMA_PORT, CHROMA_TENANT and CHROMA_DATABASE
  - server://host:port/tenant/db: no env variable used
  - server://host:port/tenant/db/coll: no env variable used
  - server://host:port/tenant/: CHROMA_DATABASE
  - server://host:port/tenant//coll: CHROMA_DATABASE
  - server://host:port//db: CHROMA_TENANT
  - server://host:port//db/coll: CHROMA_TENANT
  """

  # (1) parse uri
  pat = re.compile(r"^server://((\w+)(:(\d+))?)?/(\w+)?/(\w+)?(/(\w+))?$")

  if not (m := pat.match(uri)):
    raise ValueError(f"Invalid server URI: '{uri}'.")

  o = m.groups()

  host = v if (v := o[1]) else os.getenv("CHROMA_HOST", default_server_host)
  port = int(v if (v := o[3]) else os.getenv("CHROMA_PORT", default_server_port))
  tenant = v if (v := o[4]) else os.getenv("CHROMA_TENANT", default_tenant)
  db = v if (v := o[5]) else os.getenv("CHROMA_DATABASE", default_database)
  coll = v if (v := o[7]) else None

  # (2) return parsed uri
  return ChromioUri(
    schema="server",
    host=host,
    port=port,
    tenant=tenant,
    db=db,
    coll=coll,
  )


def __parse_cloud_uri(uri: str) -> ChromioUri:
  """Parses a cloud URI. It can be one of the following:

  - cloud:////: CHROMA_TENANT and CHROMA_DATABASE
  - cloud://///coll: CHROMA_TENANT and CHROMA_DATABASE
  - cloud:///tenant/db: no env variable used
  - cloud:///tenant/db/coll: no env variable used
  - cloud:///tenant/: CHROMA_DATABASE
  - cloud:///tenant//coll: CHROMA_DATABASE
  - cloud:////db: CHROMA_TENANT
  - cloud:////db/coll: CHROMA_TENANT
  """

  # (1) parse uri
  pat = re.compile(r"^cloud:///(\w+)?/(\w+)?(/(\w+))?$")

  if not (m := pat.match(uri)):
    raise ValueError(f"Invalid cloud URI: '{uri}'.")

  o = m.groups()

  host, port = default_cloud_host, default_cloud_port
  ten = v if (v := o[0]) else os.getenv("CHROMA_TENANT", None)
  db = v if (v := o[1]) else os.getenv("CHROMA_DATABASE", None)
  coll = v if (v := o[3]) else None

  # (2) expected tenant and database
  if ten is None or db is None:
    raise ValueError(f"Expected tenant and db in cloud URI: '/{ten or ''}/{db or ''}'.")

  # (3) return parsed uri
  return ChromioUri(
    schema="cloud",
    host=host,
    port=port,
    tenant=ten,
    db=db,
    coll=coll,
  )
