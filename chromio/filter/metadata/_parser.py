from typing import cast, override

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from ..errors import FilterSyntaxError
from ..loc import Loc
from ._antlr4.FilterParser import FilterParser as AntlrParser
from ._antlr4.Lexer import Lexer
from ._core import Cond


class _ParserErrorListener(ErrorListener):
  """Default error listener."""

  @override
  def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e) -> None:
    raise FilterSyntaxError(Loc(line, column), msg)


class MetafilterParser:
  """A parser for filters of metadata."""

  def parse(self, text: str) -> Cond:
    """Parses a given text and returns the condition defined in it.

    Args:
      text: texto to parse.

    Returns:
      Parsed expression.

    Raises:
      FilterSyntaxError: if a syntactical error found.
    """

    # (1) initialize the ANTLR4 parser to use
    input = InputStream(text)
    lexer = Lexer(input)
    tokens = CommonTokenStream(lexer)

    parser = AntlrParser(tokens)
    parser.buildParseTrees = True
    parser.removeErrorListeners()
    parser.addErrorListener(_ParserErrorListener())

    # (2) parse expression
    return cast(Cond, parser.cond())
