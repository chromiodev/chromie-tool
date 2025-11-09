import pytest

from chromio.filter.errors import FilterSyntaxError
from chromio.filter.metadata import LogicalOptor, MultiCond, Optor, Predicate
from chromio.filter.metadata import MetafilterParser as Parser


@pytest.mark.parametrize(
  ("exp", "e"),
  (
    pytest.param("dir='QT' and year=1994", LogicalOptor.AND, id="and"),
    pytest.param("dir='QT' or year=1994", LogicalOptor.OR, id="or"),
  ),
)
def test_parse_multi_predicate(parser: Parser, exp: str, e: LogicalOptor) -> None:
  """Check that parse() parses predicate and|or predicate."""

  assert parser.parse(exp) == MultiCond(
    e, [Predicate("dir", Optor.EQ, "QT"), Predicate("year", Optor.EQ, 1994)]
  )


def test_parse_raise_error_if_logical_is_not_the_same(parser: Parser) -> None:
  """Check that parse() raises error if not used the same logical operator."""

  with pytest.raises(FilterSyntaxError, match=r"must be 'and'"):
    parser.parse("dir='QT' and year=1994 or dir=1992")
