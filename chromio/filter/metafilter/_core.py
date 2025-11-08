from abc import ABC
from dataclasses import dataclass
from enum import StrEnum


class Optor(StrEnum):
  """Operators."""

  BETWEEN = "between"
  NOT_BETWEEN = "not between"
  IN = "in"
  NOT_IN = "not in"
  EQ = "=="
  NOT_EQ = "!="
  LT = "<"
  LTE = "<="
  GT = ">"
  GTE = ">="


@dataclass
class Predicate:
  """A comparison predicate of a conditional expression."""

  field: str
  """Field name to query."""

  optor: Optor
  """Comparison operator: =, !=, <, etc."""

  value: str | bool | int | list[str | bool | int]
  """Value to compare with."""


@dataclass
class Cond(ABC):
  """A conditional expression."""


@dataclass
class SimpleCond(Cond):
  """A conditional expression with only one predicate."""

  predicate: Predicate
  """Comparison predicate."""


@dataclass
class MultiCond(Cond):
  """A conditional expression with several comparison predicates."""

  predicates: list[Predicate]
