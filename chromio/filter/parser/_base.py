from abc import ABC, abstractmethod


class FilterParser(ABC):
  """A parser of data filter."""

  @abstractmethod
  def parse(self, exp: str) -> dict:
    """Parses a filter expression.

    Args:
      exp: Conditional expression to parse.

    Returns:
      The parsed expression.

    Raises:
      ValueError: if the expression is not valid.
    """
