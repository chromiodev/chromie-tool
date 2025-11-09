from typing import NamedTuple, override


class Loc(NamedTuple):
  """Location of something."""

  line: int
  """Line number."""

  col: int
  """Column number."""

  @override
  def __str__(self) -> str:
    return f"{self.line}:{self.col}"
