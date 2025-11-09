import pytest

from chromio.filter.errors import FilterSyntaxError
from chromio.filter.metadata import MetafilterParser as Parser
from chromio.filter.metadata import Optor, Predicate, SimpleCond


@pytest.mark.parametrize(
  ("text", "optor"),
  (
    pytest.param("dir = 'Quentin Tarantino'", Optor.EQ, id="="),
    pytest.param("dir == 'Quentin Tarantino'", Optor.EQ, id="=="),
    pytest.param("dir != 'Quentin Tarantino'", "!=", id="!="),
  ),
)
def test_parse_scalar_predicate(parser: Parser, text: str, optor: Optor) -> None:
  """Check that parse() parses the predicate: field operator scalar_literal."""

  assert parser.parse(text) == SimpleCond(Predicate("dir", optor, "Quentin Tarantino"))


@pytest.mark.parametrize(
  ("text", "optor"),
  (
    pytest.param("year in [1990, 1991]", Optor.IN, id="in"),
    pytest.param("year not in [1990, 1991]", Optor.NOT_IN, id="not in"),
  ),
)
def test_parse_in_predicate(parser: Parser, text: str, optor: Optor) -> None:
  """Check that parse() parses the predicate: field in [scalar, scalar...]."""

  assert parser.parse(text) == SimpleCond(Predicate("year", optor, [1990, 1991]))


@pytest.mark.parametrize(
  ("text", "optor"),
  (
    pytest.param("year between 1990 and 1999", Optor.BETWEEN, id="between"),
    pytest.param("year not between 1990 and 1999", Optor.NOT_BETWEEN, id="not between"),
  ),
)
def test_parse_between_predicate(parser: Parser, text: str, optor: Optor) -> None:
  """Check that parse() parses the predicate: field in [scalar, scalar...]."""

  assert parser.parse(text) == SimpleCond(Predicate("year", optor, [1990, 1999]))


def test_parse_not_predicate(parser: Parser) -> None:
  """Check that parse() parses the predicate: not field."""

  assert parser.parse("not closed") == SimpleCond(Predicate("closed", Optor.NOT_EQ, True))


def test_parse_bool_cmp_predicate(parser: Parser) -> None:
  """Check that parse() parses the predicate: field."""

  assert parser.parse("closed") == SimpleCond(Predicate("closed", Optor.EQ, True))


@pytest.mark.parametrize(
  ("text", "e"),
  (
    pytest.param("dir=Quentin", r"input 'dir=Quentin'", id="literal w/o quotes"),
    pytest.param("'Quentin'=dir", r"input ''Quentin''", id="literal as 1st operand"),
  ),
)
def test_parse_raises_syntax_error(parser: Parser, text: str, e: str) -> None:
  """Check that parse() raises an syntax error."""

  with pytest.raises(FilterSyntaxError, match=e):
    parser.parse(text)
