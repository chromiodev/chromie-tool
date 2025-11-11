import json


def dumps(recs: dict | list[dict], *, indent=0, sep="\n") -> str:
  """Builds a JSONL string for a record or a list of records.

  Args:
    recs: Record or records to transform.
    indent: Number of spaces to use as indentation.
    sep: Separator to use between records.
  Returns:
    A JSONL string representing the record or records.
  """

  return (
    __convert_record_to_jsonl(recs)
    if isinstance(recs, dict)
    else __convert_records_to_jsonl(recs, indent=indent, sep=sep)
  )


def __convert_record_to_jsonl(rec: dict) -> str:
  """Builds a JSONL string for a records.

  Args:
    rec: Record to transform.

  Returns:
    A JSONL string representing the record.
  """

  return json.dumps(rec, indent=None)


def __convert_records_to_jsonl(recs: list[dict], *, indent=0, sep="\n") -> str:
  """Builds a JSONL string for a list of records.

  Args:
    recs: Records to transform.
    indent: Number of spaces to use as indentation.
    sep: Separator to use between records.

  Returns:
    A JSONL string representing the records.
  """

  # (1) build representation
  repr = ""

  for i, rec in enumerate(recs):
    repr += (sep if i > 0 else "") + (" " * indent) + json.dumps(rec, indent=None)

  # (2) return representation
  return repr
