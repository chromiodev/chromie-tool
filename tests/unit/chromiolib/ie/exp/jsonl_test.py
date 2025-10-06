import pytest

import chromio.ie.exp.jsonl as jsonl


def test_convert_record_to_jsonl() -> None:
  """Check that convert_record_to_jsonl works as expected."""

  # (1) act
  out = jsonl.dumps({"a": 1, "b": 2})

  # (2) assessment
  assert out == '{"a": 1, "b": 2}'


@pytest.mark.parametrize(
  ("records", "kwargs", "e"),
  (
    pytest.param(
      [{"a": 1, "b": 2}, {"c": 3, "d": 4}],
      {},
      '{"a": 1, "b": 2}\n{"c": 3, "d": 4}',
      id="w/o indent nor sep",
    ),
    pytest.param(
      [{"a": 1, "b": 2}, {"c": 3, "d": 4}],
      {"sep": ",\n"},
      '{"a": 1, "b": 2},\n{"c": 3, "d": 4}',
      id="w/ sep",
    ),
    pytest.param(
      [{"a": 1, "b": 2}, {"c": 3, "d": 4}],
      {"indent": 2, "sep": ",\n"},
      '  {"a": 1, "b": 2},\n  {"c": 3, "d": 4}',
      id="w/ indent and sep",
    ),
  ),
)
def test_convert_records_to_jsonl(records: list[dict], kwargs: dict, e: str) -> None:
  """Check that convert_records_to_jsonl works as expected."""

  assert jsonl.dumps(records, **kwargs) == e
