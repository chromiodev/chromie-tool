from typing import override

from .loc import Loc


class FilterSyntaxError(Exception):
  """A syntax error.

  Attributes:
    loc: Error location.
  """

  def __init__(self, loc: Loc, msg: str):
    super().__init__(msg)
    self.loc = loc

  @property
  def msg(self) -> str:
    """Error message."""

    return self.args[0]

  @override
  def __str__(self) -> str:
    return f"{self.loc} {self.msg}"
