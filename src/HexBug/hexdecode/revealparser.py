from __future__ import annotations

import re

from lark.exceptions import LarkError
from lark.lark import Lark
from lark.visitors import Transformer

from . import hexast
from .hex_math import Direction

GLOOP_REGEX = re.compile(
    r"<\s*(?P<direction>[a-z_-]+)(?:\s*[, ]\s*(?P<pattern>[aqweds]+))?\s*>", re.I | re.M
)

parser = Lark(
    """
start: iota*

iota: "[" [iota ("," iota)*] "]"                -> list
    | "(" ( NUMBER "," NUMBER "," NUMBER ) ")"  -> vector
    | "HexPattern" "(" ( DIRECTION TURNS? ) ")" -> pattern
    | "NULL"                                    -> null
    | NUMBER                                    -> literal
    | UNKNOWN                                   -> unknown

TURNS: ("a"|"q"|"w"|"e"|"d")+
UNKNOWN: DIRECTION

%import common.CNAME -> DIRECTION
%import common.SIGNED_FLOAT -> NUMBER
%import common.WS
%ignore WS
"""
)


class ToAST(Transformer):
    def vector(self, args) -> hexast.Vector:
        return hexast.Vector(args[0], args[1], args[2])

    def list(self, iotas):
        return [i for i in iotas if i is not None]

    def null(self, _arguments):
        return hexast.Null()

    def literal(self, numbers):
        return numbers[0]

    def unknown(self, arguments):
        return arguments[0]

    def pattern(self, args):
        initial_direction, *maybe_turns = args
        turns = maybe_turns[0] if len(maybe_turns) > 0 else ""
        return hexast.UnknownPattern(initial_direction, turns)

    def DIRECTION(self, string):
        return Direction.from_shorthand(string)

    def UNKNOWN(self, strings):
        return hexast.Unknown("".join(strings))

    def NUMBER(self, number):
        return hexast.NumberConstant("".join(number))

    def TURNS(self, turns):
        return "".join(turns)

    def start(self, iotas):
        return iotas


def parse(text):
    # i have no clue how to modify this parser so you're getting this hack instead
    text = GLOOP_REGEX.sub(r"HexPattern(\g<direction> \g<pattern>)", text)

    try:
        tree = parser.parse(text)
        result = ToAST().transform(tree)
    except LarkError:
        return
    for child in result:
        yield child
