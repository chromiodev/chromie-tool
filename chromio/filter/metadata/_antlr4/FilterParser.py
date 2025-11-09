# Generated from Filter.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


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

def serializedATN():
    return [
        4,1,23,143,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,0,1,0,1,
        0,1,0,4,0,31,8,0,11,0,12,0,32,1,0,1,0,3,0,37,8,0,1,0,1,0,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,3,1,65,8,1,1,2,1,2,1,2,1,2,1,2,1,2,3,2,73,
        8,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,97,8,4,1,5,1,5,1,5,1,5,1,5,3,5,104,
        8,5,1,6,1,6,1,6,1,6,1,6,3,6,111,8,6,1,7,1,7,1,7,1,8,1,8,1,8,1,9,
        1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,3,10,130,8,10,1,
        11,1,11,1,11,1,11,4,11,136,8,11,11,11,12,11,137,1,11,1,11,1,11,1,
        11,0,0,12,0,2,4,6,8,10,12,14,16,18,20,22,0,1,2,0,12,12,16,16,150,
        0,36,1,0,0,0,2,64,1,0,0,0,4,72,1,0,0,0,6,74,1,0,0,0,8,96,1,0,0,0,
        10,103,1,0,0,0,12,110,1,0,0,0,14,112,1,0,0,0,16,115,1,0,0,0,18,118,
        1,0,0,0,20,129,1,0,0,0,22,131,1,0,0,0,24,25,3,2,1,0,25,26,6,0,-1,
        0,26,37,1,0,0,0,27,30,3,2,1,0,28,29,7,0,0,0,29,31,3,2,1,0,30,28,
        1,0,0,0,31,32,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,34,1,0,0,0,
        34,35,6,0,-1,0,35,37,1,0,0,0,36,24,1,0,0,0,36,27,1,0,0,0,37,38,1,
        0,0,0,38,39,5,0,0,1,39,1,1,0,0,0,40,41,3,6,3,0,41,42,6,1,-1,0,42,
        65,1,0,0,0,43,44,5,15,0,0,44,45,3,6,3,0,45,46,6,1,-1,0,46,65,1,0,
        0,0,47,48,3,6,3,0,48,49,3,8,4,0,49,50,3,20,10,0,50,51,6,1,-1,0,51,
        65,1,0,0,0,52,53,3,6,3,0,53,54,3,10,5,0,54,55,3,22,11,0,55,56,6,
        1,-1,0,56,65,1,0,0,0,57,58,3,6,3,0,58,59,3,12,6,0,59,60,3,4,2,0,
        60,61,5,12,0,0,61,62,3,4,2,0,62,63,6,1,-1,0,63,65,1,0,0,0,64,40,
        1,0,0,0,64,43,1,0,0,0,64,47,1,0,0,0,64,52,1,0,0,0,64,57,1,0,0,0,
        65,3,1,0,0,0,66,67,3,16,8,0,67,68,6,2,-1,0,68,73,1,0,0,0,69,70,3,
        18,9,0,70,71,6,2,-1,0,71,73,1,0,0,0,72,66,1,0,0,0,72,69,1,0,0,0,
        73,5,1,0,0,0,74,75,5,21,0,0,75,76,6,3,-1,0,76,7,1,0,0,0,77,78,5,
        2,0,0,78,97,6,4,-1,0,79,80,5,3,0,0,80,97,6,4,-1,0,81,82,5,4,0,0,
        82,97,6,4,-1,0,83,84,5,5,0,0,84,97,6,4,-1,0,85,86,5,6,0,0,86,97,
        6,4,-1,0,87,88,5,7,0,0,88,97,6,4,-1,0,89,90,5,8,0,0,90,97,6,4,-1,
        0,91,92,5,13,0,0,92,97,6,4,-1,0,93,94,5,15,0,0,94,95,5,13,0,0,95,
        97,6,4,-1,0,96,77,1,0,0,0,96,79,1,0,0,0,96,81,1,0,0,0,96,83,1,0,
        0,0,96,85,1,0,0,0,96,87,1,0,0,0,96,89,1,0,0,0,96,91,1,0,0,0,96,93,
        1,0,0,0,97,9,1,0,0,0,98,99,5,14,0,0,99,104,6,5,-1,0,100,101,5,15,
        0,0,101,102,5,14,0,0,102,104,6,5,-1,0,103,98,1,0,0,0,103,100,1,0,
        0,0,104,11,1,0,0,0,105,106,5,13,0,0,106,111,6,6,-1,0,107,108,5,15,
        0,0,108,109,5,13,0,0,109,111,6,6,-1,0,110,105,1,0,0,0,110,107,1,
        0,0,0,111,13,1,0,0,0,112,113,7,0,0,0,113,114,6,7,-1,0,114,15,1,0,
        0,0,115,116,5,17,0,0,116,117,6,8,-1,0,117,17,1,0,0,0,118,119,5,18,
        0,0,119,120,6,9,-1,0,120,19,1,0,0,0,121,122,3,16,8,0,122,123,6,10,
        -1,0,123,130,1,0,0,0,124,125,3,18,9,0,125,126,6,10,-1,0,126,130,
        1,0,0,0,127,128,5,20,0,0,128,130,6,10,-1,0,129,121,1,0,0,0,129,124,
        1,0,0,0,129,127,1,0,0,0,130,21,1,0,0,0,131,132,5,9,0,0,132,135,3,
        20,10,0,133,134,5,11,0,0,134,136,3,20,10,0,135,133,1,0,0,0,136,137,
        1,0,0,0,137,135,1,0,0,0,137,138,1,0,0,0,138,139,1,0,0,0,139,140,
        5,10,0,0,140,141,6,11,-1,0,141,23,1,0,0,0,9,32,36,64,72,96,103,110,
        129,137
    ]

class FilterParser ( Parser ):

    grammarFileName = "Filter.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "'='", "'=='", "'!='", "'<'", "'<='", 
                     "'>'", "'>='", "'['", "']'", "','" ]

    symbolicNames = [ "<INVALID>", "DOT", "EQ", "EQ2", "NOT_EQ", "LA_BRACKET", 
                      "LA_BRACKET_EQ", "RA_BRACKET", "RA_BRACKET_EQ", "LBRACKET", 
                      "RBRACKET", "COMMA", "AND", "BETWEEN", "IN", "NOT", 
                      "OR", "LITERAL_TEXT", "LITERAL_INT", "LITERAL_REAL", 
                      "LITERAL_BOOL", "ID", "WHITESPACE", "BACKSLASH" ]

    RULE_cond = 0
    RULE_predicate = 1
    RULE_between_value = 2
    RULE_field = 3
    RULE_cmp_optor = 4
    RULE_in_optor = 5
    RULE_between_optor = 6
    RULE_bin_logical_optor = 7
    RULE_literal_text = 8
    RULE_literal_num = 9
    RULE_literal_scalar = 10
    RULE_literal_list = 11

    ruleNames =  [ "cond", "predicate", "between_value", "field", "cmp_optor", 
                   "in_optor", "between_optor", "bin_logical_optor", "literal_text", 
                   "literal_num", "literal_scalar", "literal_list" ]

    EOF = Token.EOF
    DOT=1
    EQ=2
    EQ2=3
    NOT_EQ=4
    LA_BRACKET=5
    LA_BRACKET_EQ=6
    RA_BRACKET=7
    RA_BRACKET_EQ=8
    LBRACKET=9
    RBRACKET=10
    COMMA=11
    AND=12
    BETWEEN=13
    IN=14
    NOT=15
    OR=16
    LITERAL_TEXT=17
    LITERAL_INT=18
    LITERAL_REAL=19
    LITERAL_BOOL=20
    ID=21
    WHITESPACE=22
    BACKSLASH=23

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class CondContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._predicate = None # PredicateContext
            self.p = list() # of PredicateContexts
            self._AND = None # Token
            self.o = list() # of Tokens
            self._OR = None # Token
            self._tset50 = None # Token

        def EOF(self):
            return self.getToken(FilterParser.EOF, 0)

        def predicate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FilterParser.PredicateContext)
            else:
                return self.getTypedRuleContext(FilterParser.PredicateContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(FilterParser.AND)
            else:
                return self.getToken(FilterParser.AND, i)

        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(FilterParser.OR)
            else:
                return self.getToken(FilterParser.OR, i)

        def getRuleIndex(self):
            return FilterParser.RULE_cond




    def cond(self):

        localctx = FilterParser.CondContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cond)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 24
                localctx._predicate = self.predicate()
                return SimpleCond(localctx._predicate)
                pass

            elif la_ == 2:
                self.state = 27
                localctx._predicate = localctx._predicate = self.predicate()
                localctx.p.append(localctx._predicate)
                self.state = 30 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 28
                    localctx._tset50 = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==12 or _la==16):
                        localctx._tset50 = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    localctx.o.append(localctx._tset50)
                    self.state = 29
                    localctx._predicate = localctx._predicate = self.predicate()
                    localctx.p.append(localctx._predicate)
                    self.state = 32 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==12 or _la==16):
                        break

                return multi_cond(localctx.o, localctx.p)
                pass


            self.state = 38
            self.match(FilterParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._field = None # FieldContext
            self._cmp_optor = None # Cmp_optorContext
            self._literal_scalar = None # Literal_scalarContext
            self._in_optor = None # In_optorContext
            self._literal_list = None # Literal_listContext
            self._between_optor = None # Between_optorContext
            self._between_value = None # Between_valueContext
            self.i = list() # of Between_valueContexts

        def field(self):
            return self.getTypedRuleContext(FilterParser.FieldContext,0)


        def NOT(self):
            return self.getToken(FilterParser.NOT, 0)

        def cmp_optor(self):
            return self.getTypedRuleContext(FilterParser.Cmp_optorContext,0)


        def literal_scalar(self):
            return self.getTypedRuleContext(FilterParser.Literal_scalarContext,0)


        def in_optor(self):
            return self.getTypedRuleContext(FilterParser.In_optorContext,0)


        def literal_list(self):
            return self.getTypedRuleContext(FilterParser.Literal_listContext,0)


        def between_optor(self):
            return self.getTypedRuleContext(FilterParser.Between_optorContext,0)


        def AND(self):
            return self.getToken(FilterParser.AND, 0)

        def between_value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FilterParser.Between_valueContext)
            else:
                return self.getTypedRuleContext(FilterParser.Between_valueContext,i)


        def getRuleIndex(self):
            return FilterParser.RULE_predicate




    def predicate(self):

        localctx = FilterParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_predicate)
        try:
            self.state = 64
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 40
                localctx._field = self.field()
                return Predicate(localctx._field, "==", True)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.match(FilterParser.NOT)
                self.state = 44
                localctx._field = self.field()
                return Predicate(localctx._field, "!=", True)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 47
                localctx._field = self.field()
                self.state = 48
                localctx._cmp_optor = self.cmp_optor()
                self.state = 49
                localctx._literal_scalar = self.literal_scalar()
                return Predicate(localctx._field, localctx._cmp_optor, localctx._literal_scalar)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 52
                localctx._field = self.field()
                self.state = 53
                localctx._in_optor = self.in_optor()
                self.state = 54
                localctx._literal_list = self.literal_list()
                return Predicate(localctx._field, localctx._in_optor, localctx._literal_list)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 57
                localctx._field = self.field()
                self.state = 58
                localctx._between_optor = self.between_optor()
                self.state = 59
                localctx._between_value = self.between_value()
                localctx.i.append(localctx._between_value)
                self.state = 60
                self.match(FilterParser.AND)
                self.state = 61
                localctx._between_value = self.between_value()
                localctx.i.append(localctx._between_value)
                return Predicate(localctx._field, localctx._between_optor, localctx.i)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Between_valueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._literal_text = None # Literal_textContext
            self._literal_num = None # Literal_numContext

        def literal_text(self):
            return self.getTypedRuleContext(FilterParser.Literal_textContext,0)


        def literal_num(self):
            return self.getTypedRuleContext(FilterParser.Literal_numContext,0)


        def getRuleIndex(self):
            return FilterParser.RULE_between_value




    def between_value(self):

        localctx = FilterParser.Between_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_between_value)
        try:
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                localctx._literal_text = self.literal_text()
                return localctx._literal_text
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                localctx._literal_num = self.literal_num()
                return localctx._literal_num
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def ID(self):
            return self.getToken(FilterParser.ID, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_field




    def field(self):

        localctx = FilterParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            localctx.name = self.match(FilterParser.ID)
            return (None if localctx.name is None else localctx.name.text)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cmp_optorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(FilterParser.EQ, 0)

        def EQ2(self):
            return self.getToken(FilterParser.EQ2, 0)

        def NOT_EQ(self):
            return self.getToken(FilterParser.NOT_EQ, 0)

        def LA_BRACKET(self):
            return self.getToken(FilterParser.LA_BRACKET, 0)

        def LA_BRACKET_EQ(self):
            return self.getToken(FilterParser.LA_BRACKET_EQ, 0)

        def RA_BRACKET(self):
            return self.getToken(FilterParser.RA_BRACKET, 0)

        def RA_BRACKET_EQ(self):
            return self.getToken(FilterParser.RA_BRACKET_EQ, 0)

        def BETWEEN(self):
            return self.getToken(FilterParser.BETWEEN, 0)

        def NOT(self):
            return self.getToken(FilterParser.NOT, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_cmp_optor




    def cmp_optor(self):

        localctx = FilterParser.Cmp_optorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_cmp_optor)
        try:
            self.state = 96
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 77
                self.match(FilterParser.EQ)
                return Optor.EQ
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.match(FilterParser.EQ2)
                return Optor.EQ
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 81
                self.match(FilterParser.NOT_EQ)
                return Optor.NOT_EQ
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 83
                self.match(FilterParser.LA_BRACKET)
                return Optor.LT
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 5)
                self.state = 85
                self.match(FilterParser.LA_BRACKET_EQ)
                return Optor.LTE
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 6)
                self.state = 87
                self.match(FilterParser.RA_BRACKET)
                return Optor.GT
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 7)
                self.state = 89
                self.match(FilterParser.RA_BRACKET_EQ)
                return Optor.GTE
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 8)
                self.state = 91
                self.match(FilterParser.BETWEEN)
                return Optor.BETWEEN
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 9)
                self.state = 93
                self.match(FilterParser.NOT)
                self.state = 94
                self.match(FilterParser.BETWEEN)
                return Optor.NOT_BETWEEN
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class In_optorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IN(self):
            return self.getToken(FilterParser.IN, 0)

        def NOT(self):
            return self.getToken(FilterParser.NOT, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_in_optor




    def in_optor(self):

        localctx = FilterParser.In_optorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_in_optor)
        try:
            self.state = 103
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 98
                self.match(FilterParser.IN)
                return Optor.IN
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 100
                self.match(FilterParser.NOT)
                self.state = 101
                self.match(FilterParser.IN)
                return Optor.NOT_IN
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Between_optorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BETWEEN(self):
            return self.getToken(FilterParser.BETWEEN, 0)

        def NOT(self):
            return self.getToken(FilterParser.NOT, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_between_optor




    def between_optor(self):

        localctx = FilterParser.Between_optorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_between_optor)
        try:
            self.state = 110
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13]:
                self.enterOuterAlt(localctx, 1)
                self.state = 105
                self.match(FilterParser.BETWEEN)
                return Optor.BETWEEN
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 107
                self.match(FilterParser.NOT)
                self.state = 108
                self.match(FilterParser.BETWEEN)
                return Optor.NOT_BETWEEN
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Bin_logical_optorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.optor = None # Token

        def AND(self):
            return self.getToken(FilterParser.AND, 0)

        def OR(self):
            return self.getToken(FilterParser.OR, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_bin_logical_optor




    def bin_logical_optor(self):

        localctx = FilterParser.Bin_logical_optorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_bin_logical_optor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            localctx.optor = self._input.LT(1)
            _la = self._input.LA(1)
            if not(_la==12 or _la==16):
                localctx.optor = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            return (None if localctx.optor is None else localctx.optor.text)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Literal_textContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None # Token

        def LITERAL_TEXT(self):
            return self.getToken(FilterParser.LITERAL_TEXT, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_literal_text




    def literal_text(self):

        localctx = FilterParser.Literal_textContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_literal_text)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            localctx.val = self.match(FilterParser.LITERAL_TEXT)
            return (None if localctx.val is None else localctx.val.text)[1:-1]
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Literal_numContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None # Token

        def LITERAL_INT(self):
            return self.getToken(FilterParser.LITERAL_INT, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_literal_num




    def literal_num(self):

        localctx = FilterParser.Literal_numContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_literal_num)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            localctx.val = self.match(FilterParser.LITERAL_INT)
            return int((None if localctx.val is None else localctx.val.text))
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Literal_scalarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._literal_text = None # Literal_textContext
            self._literal_num = None # Literal_numContext
            self._LITERAL_BOOL = None # Token

        def literal_text(self):
            return self.getTypedRuleContext(FilterParser.Literal_textContext,0)


        def literal_num(self):
            return self.getTypedRuleContext(FilterParser.Literal_numContext,0)


        def LITERAL_BOOL(self):
            return self.getToken(FilterParser.LITERAL_BOOL, 0)

        def getRuleIndex(self):
            return FilterParser.RULE_literal_scalar




    def literal_scalar(self):

        localctx = FilterParser.Literal_scalarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_literal_scalar)
        try:
            self.state = 129
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 121
                localctx._literal_text = self.literal_text()
                return localctx._literal_text
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                localctx._literal_num = self.literal_num()
                return localctx._literal_num
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 3)
                self.state = 127
                localctx._LITERAL_BOOL = self.match(FilterParser.LITERAL_BOOL)
                return (None if localctx._LITERAL_BOOL is None else localctx._LITERAL_BOOL.text) == 'true'
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Literal_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._literal_scalar = None # Literal_scalarContext
            self.items = list() # of Literal_scalarContexts

        def LBRACKET(self):
            return self.getToken(FilterParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(FilterParser.RBRACKET, 0)

        def literal_scalar(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FilterParser.Literal_scalarContext)
            else:
                return self.getTypedRuleContext(FilterParser.Literal_scalarContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(FilterParser.COMMA)
            else:
                return self.getToken(FilterParser.COMMA, i)

        def getRuleIndex(self):
            return FilterParser.RULE_literal_list




    def literal_list(self):

        localctx = FilterParser.Literal_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_literal_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(FilterParser.LBRACKET)
            self.state = 132
            localctx._literal_scalar = self.literal_scalar()
            localctx.items.append(localctx._literal_scalar)
            self.state = 135 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 133
                self.match(FilterParser.COMMA)
                self.state = 134
                localctx._literal_scalar = self.literal_scalar()
                localctx.items.append(localctx._literal_scalar)
                self.state = 137 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==11):
                    break

            self.state = 139
            self.match(FilterParser.RBRACKET)
            return localctx.items
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





