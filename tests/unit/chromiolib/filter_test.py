import pytest

from chromio.filter import MetaFilterParser


@pytest.fixture(scope="module")
def parser() -> MetaFilterParser:
  """Metafilter parser to use in the tests."""

  return MetaFilterParser()


@pytest.mark.parametrize(
  ("exp", "e"),
  (
    pytest.param("field=Lu To", {"field": {"$eq": "Lu To"}}, id="ws"),
    pytest.param("field=value", {"field": {"$eq": "value"}}, id="="),
    pytest.param("field!=value", {"field": {"$ne": "value"}}, id="!="),
    pytest.param("field<value", {"field": {"$lt": "value"}}, id="<"),
    pytest.param("field<=value", {"field": {"$lte": "value"}}, id="<="),
    pytest.param("field>value", {"field": {"$gt": "value"}}, id=">"),
    pytest.param("field>=value", {"field": {"$gte": "value"}}, id=">="),
  ),
)
def test_parse_valid_exp(parser: MetaFilterParser, exp: str, e: dict) -> None:
  """Check that parse() parses a valid filter expression."""

  assert parser.parse(exp) == e


@pytest.mark.parametrize(
  ("exp",),
  (
    pytest.param("field", id="only field"),
    pytest.param("field|value", id="invalid operator"),
  ),
)
def test_parse_invalid_exp(parser: MetaFilterParser, exp: str) -> None:
  """Check that parse() raises an error if invalid expression."""

  with pytest.raises(ValueError, match=f"Invalid metafilter: '{exp}'."):
    parser.parse(exp)
