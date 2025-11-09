from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, override


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


class LogicalOptor(StrEnum):
  """A logical operator."""

  AND = "and"
  OR = "or"


@dataclass
class Predicate:
  """A comparison predicate of a conditional expression."""

  field: str
  """Field name to query."""

  optor: Optor
  """Comparison operator: =, !=, <, etc."""

  value: str | bool | int | list[str | bool | int]
  """Value to compare with."""

  def to_chroma(self) -> dict[str, Any]:
    """Returns the predicate in a Chroma object such as, for example,
    {"dir": {"$eq": "Quentin Tarantino"}}.
    """

    # (1) pre
    field, optor, value = self.field, self.optor, self.value

    match optor:
      case Optor.EQ:
        return {field: value}
      case Optor.NOT_EQ:
        return {field: {"$ne": value}}
      case Optor.LT:
        return {field: {"$lt": value}}
      case Optor.LTE:
        return {field: {"$lte": value}}
      case Optor.GT:
        return {field: {"$gt": value}}
      case Optor.GTE:
        return {field: {"$gte": value}}
      case Optor.IN:
        return {field: {"$in": value}}
      case Optor.NOT_IN:
        return {field: {"$nin": value}}
      case Optor.BETWEEN:
        return {"$and": [{field: {"$gte": value[0]}}, {field: {"$lte": value[1]}}]}  # type: ignore
      case Optor.NOT_BETWEEN:
        return {"$and": [{field: {"$lt": value[0]}}, {field: {"$gt": value[1]}}]}  # type: ignore
      case _:  # pragma: no cover
        raise Exception("Internal error: unknown operator.")


@dataclass
class Cond(ABC):
  """A conditional expression."""

  @abstractmethod
  def to_chroma(self) -> dict[str, Any]:
    """Returns the condition in a Chroma object."""


@dataclass
class SimpleCond(Cond):
  """A conditional expression with only one predicate."""

  predicate: Predicate
  """Comparison predicate."""

  @override
  def to_chroma(self) -> dict[str, Any]:
    return self.predicate.to_chroma()


@dataclass
class MultiCond(Cond):
  """A conditional expression with several comparison predicates."""

  optor: LogicalOptor
  """Logical operator to use."""

  predicates: list[Predicate]
  """Predicates associated to this conditional expression."""

  @override
  def to_chroma(self) -> dict[str, Any]:
    return {
      {LogicalOptor.AND: "$and", LogicalOptor.OR: "$or"}[self.optor]: [
        p.to_chroma() for p in self.predicates
      ]
    }
