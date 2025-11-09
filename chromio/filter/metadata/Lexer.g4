lexer grammar Lexer;

options {
  language = Python3;
}

@lexer::header {

}


///////////////
// fragments //
///////////////
fragment A: [aA];
fragment B: [bB];
fragment D: [dD];
fragment E: [eE];
fragment I: [iI];
fragment N: [nN];
fragment O: [oO];
fragment R: [rR];
fragment T: [tT];
fragment W: [wW];


fragment LETTER: [a-zA-Z];
fragment DEC_DIGIT: [0-9];

fragment SQUOTE: '\'';
fragment DQUOTE: '"';
fragment UNDERSCORE: '_';

fragment ESC_CHAR: '\\' [btrn'"\\];


/////////////
// Symbols //
/////////////

DOT: '.';
EQ: '=';
EQ2: '==';
NOT_EQ: '!=';
LA_BRACKET: '<';
LA_BRACKET_EQ: '<='; 
RA_BRACKET: '>';
RA_BRACKET_EQ: '>=';
LBRACKET: '[';
RBRACKET: ']';
COMMA: ',';


//////////////
// Keywords //
//////////////

AND: A N D;
BETWEEN: B E T W E E N;
IN: I N;
NOT: N O T;
OR: O R;


//////////////
// Literals //
//////////////

LITERAL_TEXT: SQUOTE (ESC_CHAR|.)*? SQUOTE | DQUOTE (ESC_CHAR|.)*? DQUOTE;
LITERAL_INT: DEC_DIGIT+;
LITERAL_REAL: LITERAL_INT DOT DEC_DIGIT*;


///////////
// Names //
///////////

ID: (LETTER | UNDERSCORE) (LETTER | UNDERSCORE | DEC_DIGIT)*;


/////////////////
// Whitespaces //
/////////////////

WHITESPACE: [ \t] -> skip;
BACKSLASH: '\\' '\r'? '\n' -> skip;
