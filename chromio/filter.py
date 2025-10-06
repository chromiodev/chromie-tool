import re
from abc import ABC, abstractmethod
from typing import override


class FilterParser(ABC):
  """A parser of data filter."""

  @abstractmethod
  def parse(self, exp: str) -> dict:
    """Parses a filter expression.

    Args:
      exp: Conditional expression to parse.

    Returns:
      The parsed expression.

    Raises:
      ValueError: if the expression is not valid.
    """


class MetaFilterParser(FilterParser):
  """A filter by metadata."""

  operator_map = {
    "=": "$eq",
    "!=": "$ne",
    "<": "$lt",
    "<=": "$lte",
    ">": "$gt",
    ">=": "$gte",
  }

  @override
  def parse(self, exp: str) -> dict:
    # (1) parse
    pat = re.compile(r"^(\w+)(=|!=|<|<=|>|>=)([ \w]+)$")

    if not (m := pat.match(exp)):
      raise ValueError(f"Invalid metafilter: '{exp}'.")

    o = m.groups()

    # (2) return
    return {o[0]: {MetaFilterParser.operator_map[o[1]]: o[2]}}
