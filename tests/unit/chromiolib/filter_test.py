import pytest

from chromio.filter import MetaFilterParser


@pytest.fixture(scope="module")
def parser() -> MetaFilterParser:
  """Metafilter parser to use in the tests."""

  return MetaFilterParser()


@pytest.mark.parametrize(
  ("exp", "e"),
  (
    pytest.param("fld=true", {"fld": {"$eq": True}}, id="true"),
    pytest.param("fld=True", {"fld": {"$eq": True}}, id="True"),
    pytest.param("fld=false", {"fld": {"$eq": False}}, id="false"),
    pytest.param("fld=False", {"fld": {"$eq": False}}, id="False"),
    pytest.param("fld=123", {"fld": {"$eq": 123}}, id="int"),
    pytest.param("fld='va l ue'", {"fld": {"$eq": "va l ue"}}, id="'text'"),
    pytest.param("fld=value", {"fld": {"$eq": "value"}}, id="="),
    pytest.param("fld!=value", {"fld": {"$ne": "value"}}, id="!="),
    pytest.param("fld<value", {"fld": {"$lt": "value"}}, id="<"),
    pytest.param("fld<=value", {"fld": {"$lte": "value"}}, id="<="),
    pytest.param("fld>value", {"fld": {"$gt": "value"}}, id=">"),
    pytest.param("fld>=value", {"fld": {"$gte": "value"}}, id=">="),
    pytest.param(
      "f=1 and g=2",
      {"$and": [{"f": {"$eq": 1}}, {"g": {"$eq": 2}}]},
      id="p and p",
    ),
    pytest.param(
      "f=1 or f=2",
      {"$or": [{"f": {"$eq": 1}}, {"f": {"$eq": 2}}]},
      id="p or p",
    ),
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
    pytest.param("f=v and g=v or h=v", id="multi-predicate"),
  ),
)
def test_parse_invalid_exp(parser: MetaFilterParser, exp: str) -> None:
  """Check that parse() raises an error if invalid expression."""

  with pytest.raises(ValueError, match=f"Invalid metafilter: {exp}"):
    parser.parse(exp)
