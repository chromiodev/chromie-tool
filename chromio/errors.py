from abc import ABC


class ChromieError(Exception, ABC):
  """An error related to Chromie."""

  def __init__(self, msg: str):
    super().__init__(msg)

  @property
  def msg(self) -> str:  # pragma: no cover
    """Error message."""

    return self.args[0]


class ChromieInternalError(ChromieError):  # pragma: no cover
  """An internal error."""


class CollNotFoundError(ChromieError):
  """A collection not found when it should exist."""

  def __init__(self, name: str):
    super().__init__(f"Collection '{name}' not found.")
    self.coll_name = name


class CollAlreadyExistsError(ChromieError):
  """Indicates that a collection already exists when this shouldn't."""

  def __init__(self, name: str):
    super().__init__(f"Collection '{name}' already exists.")
    self.coll_name = name
