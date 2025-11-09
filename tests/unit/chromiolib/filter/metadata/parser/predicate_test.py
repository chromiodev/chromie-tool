import pytest

from chromio.filter.errors import FilterSyntaxError
from chromio.filter.metadata import MetafilterParser as Parser
from chromio.filter.metadata import Optor, Predicate, SimpleCond


@pytest.mark.parametrize(
  ("text", "optor"),
  (
    pytest.param("year = 2000", Optor.EQ, id="="),
    pytest.param("year == 2000", Optor.EQ, id="=="),
    pytest.param("year != 2000", Optor.NOT_EQ, id="!="),
    pytest.param("year < 2000", Optor.LT, id="<"),
    pytest.param("year <= 2000", Optor.LTE, id="<="),
    pytest.param("year > 2000", Optor.GT, id=">"),
    pytest.param("year >= 2000", Optor.GTE, id=">="),
  ),
)
def test_parse_num_predicate(parser: Parser, text: str, optor: Optor) -> None:
  """Check that parse() parses the predicate: field operator literal_number."""

  assert parser.parse(text) == SimpleCond(Predicate("year", optor, 2000))


@pytest.mark.parametrize(
  ("text", "optor"),
  (
    pytest.param("dir = 'QT'", Optor.EQ, id="="),
    pytest.param("dir == 'QT'", Optor.EQ, id="=="),
    pytest.param("dir != 'QT'", Optor.NOT_EQ, id="!="),
  ),
)
def test_parse_textual_predicate(parser: Parser, text: str, optor: Optor) -> None:
  """Check that parse() parses the predicate: field operator literal_number."""

  assert parser.parse(text) == SimpleCond(Predicate("dir", optor, "QT"))


@pytest.mark.parametrize(
  ("text", "e_optor", "e_value"),
  (
    pytest.param("closed", Optor.EQ, True, id="field"),
    pytest.param("not closed", Optor.NOT_EQ, True, id="not field"),
    pytest.param("closed = true", Optor.EQ, True, id="field = true"),
    pytest.param("closed == true", Optor.EQ, True, id="field == true"),
    pytest.param("closed = false", Optor.EQ, False, id="field = false"),
    pytest.param("closed == false", Optor.EQ, False, id="field == false"),
  ),
)
def test_parse_bool_predicate(
  parser: Parser,
  text: str,
  e_optor: Optor,
  e_value: bool,
) -> None:
  """Check that parse() parses the predicate: field."""

  assert parser.parse(text) == SimpleCond(Predicate("closed", e_optor, e_value))


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
