import re
from typing import override

from ._base import FilterParser


class MetaFilterParser(FilterParser):
  """A filter by metadata."""

  @override
  def parse(self, exp: str) -> dict:
    PREDICATE = r"(\w+)(=|!=|<|<=|>|>=)((\w+)|('[^']*'))"

    if (m := re.compile(rf"^{PREDICATE}$").match(exp)) is not None:
      return _parse_predicate(m)
    elif m := re.compile(rf"^{PREDICATE} +(and|or) +{PREDICATE}$").match(exp):
      return _parse_predicates(m)
    else:
      raise ValueError(f"Invalid metafilter: {exp}")


def _parse_predicate(m: re.Match[str]) -> dict:
  """Parses a filter with only one predicate.

  Args:
    m: Predicate regular expression.

  Returns:
    The Chroma filter.
  """

  return _build_chroma_predicate(*(m.groups()[0:3]))


def _parse_predicates(m: re.Match[str]) -> dict:
  """Parses a filter with two predicates.

  Args:
    m: Regular expression.

  Returns:
    The Chroma filter.
  """

  # (1) decompose expression
  g = m.groups()

  f1, o1, v1 = g[0:3]
  logical = g[5]
  f2, o2, v2 = g[6:9]

  # (2) return Chroma filter
  return {
    "$" + logical: [
      _build_chroma_predicate(f1, o1, v1),
      _build_chroma_predicate(f2, o2, v2),
    ]
  }


def _parse_value(v: str) -> bool | int | str:
  """Parses a given predicate value. This can be a bool, int or string.

  Args:
    v: Value to parse.

  Returns:
    The value.
  """

  match v:
    case "true" | "True":
      return True
    case "false" | "False":
      return False
    case v if v.isdigit():
      return int(v)
    case v if v.startswith("'") and v.endswith("'"):
      return v[1:-1]
    case _:
      return v


def _build_chroma_predicate(field: str, optor: str, value: str) -> dict:
  """Parses a Chroma filter with the field, the operator and the value."""

  OPERATOR_MAP = {
    "=": "$eq",
    "!=": "$ne",
    "<": "$lt",
    "<=": "$lte",
    ">": "$gt",
    ">=": "$gte",
  }

  return {field: {OPERATOR_MAP[optor]: _parse_value(value)}}
