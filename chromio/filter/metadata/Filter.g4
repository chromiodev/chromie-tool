grammar Filter;

options {
  tokenVocab = Lexer;
  language = Python3;
}

@parser::header {
from .._core import *
from ...loc import Loc
from ...errors import FilterSyntaxError

def multi_cond(optors: LogicalOptor, predicates: list[Predicate]) -> MultiCond:
  """Builds a MultiCond."""

  # (1) arrange
  optors = [o.text for o in optors]

  # (2) check that all the operators are the same
  optor = optors[0]

  for o in optors[1:]:
    if optor != o:
      raise FilterSyntaxError(
        Loc(0, 0),
        f"All the logical operators must be '{optor}'."
      )

  # (3) build
  return MultiCond(optor, predicates)
}

/// A filter expression.
cond: (
  predicate {return SimpleCond($predicate.ctx)}
  | p+=predicate (o+=(AND|OR) p+=predicate)+ {return multi_cond($o, $p)}
) EOF
;

/// A predicate, that is, a simple condition.
predicate:
  field {return Predicate($field.ctx, "==", True)}
  | NOT field {return Predicate($field.ctx, "!=", True)}
  | field cmp_optor literal_scalar {return Predicate($field.ctx, $cmp_optor.ctx, $literal_scalar.ctx)}
  | field in_optor literal_list {return Predicate($field.ctx, $in_optor.ctx, $literal_list.ctx)}
  | field between_optor i+=between_value AND i+=between_value {return Predicate($field.ctx, $between_optor.ctx, $i)}
;

between_value:
  literal_text {return $literal_text.ctx}
  | literal_num {return $literal_num.ctx}
;


/// A field to query.
field: name=ID {return $name.text};

/// A comparison operator.
cmp_optor:
  EQ {return Optor.EQ}
  | EQ2 {return Optor.EQ}
  | NOT_EQ {return Optor.NOT_EQ}
  | LA_BRACKET {return Optor.LT}
  | LA_BRACKET_EQ {return Optor.LTE}
  | RA_BRACKET {return Optor.GT}
  | RA_BRACKET_EQ {return Optor.GTE}
  | BETWEEN {return Optor.BETWEEN}
  | NOT BETWEEN {return Optor.NOT_BETWEEN}
;

/// An in operator.
in_optor:
  IN {return Optor.IN}
  | NOT IN {return Optor.NOT_IN}
;

/// A between operator.
between_optor:
  BETWEEN {return Optor.BETWEEN}
  | NOT BETWEEN {return Optor.NOT_BETWEEN}
;


/// A logical operator.
bin_logical_optor: optor=(AND | OR) {return $optor.text};

/// A literal.
literal_text: val=LITERAL_TEXT {return $val.text[1:-1]};
literal_num: val=LITERAL_INT {return int($val.text)};

literal_scalar:
  literal_text {return $literal_text.ctx}
  | literal_num {return $literal_num.ctx}
  | LITERAL_BOOL {return $LITERAL_BOOL.text == 'true'}
;

/// A list literal: [...].
literal_list:
  LBRACKET items+=literal_scalar (COMMA items+=literal_scalar)+ RBRACKET {return $items}
;
