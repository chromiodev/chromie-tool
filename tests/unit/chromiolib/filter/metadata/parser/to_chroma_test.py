from typing import Any

import pytest

from chromio.filter.metadata import LogicalOptor, MultiCond, Optor, Predicate, SimpleCond


@pytest.mark.parametrize(
  ("args", "e"),
  (
    pytest.param(("dir", Optor.EQ, "QT"), {"dir": "QT"}, id="="),
    pytest.param(("dir", Optor.NOT_EQ, "QT"), {"dir": {"$ne": "QT"}}, id="!="),
    pytest.param(("y", Optor.LT, 2000), {"y": {"$lt": 2000}}, id="<"),
    pytest.param(("y", Optor.LTE, 2000), {"y": {"$lte": 2000}}, id="<="),
    pytest.param(("y", Optor.GT, 2000), {"y": {"$gt": 2000}}, id=">"),
    pytest.param(("y", Optor.GTE, 2000), {"y": {"$gte": 2000}}, id=">="),
    pytest.param(("y", Optor.IN, [2000, 2001]), {"y": {"$in": [2000, 2001]}}, id="in"),
    pytest.param(
      ("y", Optor.NOT_IN, [2000, 2001]),
      {"y": {"$nin": [2000, 2001]}},
      id="not in",
    ),
    pytest.param(
      ("y", Optor.BETWEEN, [2000, 2010]),
      {"$and": [{"y": {"$gte": 2000}}, {"y": {"$lte": 2010}}]},
      id="between",
    ),
    pytest.param(
      ("y", Optor.NOT_BETWEEN, [2000, 2010]),
      {"$and": [{"y": {"$lt": 2000}}, {"y": {"$gt": 2010}}]},
      id="not between",
    ),
  ),
)
def test_predicate_to_chroma(args: tuple[str, Optor, Any], e: dict[str, Any]) -> None:
  """Check that Predicate.to_chroma() translates ok."""

  assert Predicate(*args).to_chroma() == e


def test_simple_cond_to_chroma() -> None:
  """Check that SimpleCond.to_chroma() translates ok."""

  assert SimpleCond(Predicate("dir", Optor.EQ, "QT")).to_chroma() == {"dir": "QT"}


def test_multi_cond_to_chroma() -> None:
  """Check that MultiCond.to_chroma() translates ok."""

  assert MultiCond(
    LogicalOptor.AND,
    [Predicate("dir", Optor.EQ, "QT"), Predicate("year", Optor.EQ, 1994)],
  ).to_chroma() == {"$and": [{"dir": "QT"}, {"year": 1994}]}
