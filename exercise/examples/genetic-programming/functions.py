import math
from dataclasses import dataclass
from typing import Any
import operator

@dataclass
class Function():
    name: str
    arity: int
    function: callable

    def __init__(self, arity_, name_, function_):
        self.function = function_
        self.name = name_
        self.arity = arity_

    def __str__(self):
        return self.name

    def call(self, args: list) -> Any:
        assert (len(args) == self.arity)
        return self.function(*args)

def f2b(input: float):
    return True if input > 0 else False

def b2f(input: bool):
    return 1.0 if input else -1.0

def pdiv(x, y):
    return x / y if y > 0 else 1.0

def log10(x):
    return math.log10(x) if x > 0 else x

def log2(x):
    return math.log2(x) if x > 0 else x

def sqrt(x):
    return math.sqrt(x) if x > 0 else x

def mod(x,y):
    return operator.mod(x,y) if y > 0 else x


# Arithmetic Functions
ADD = Function(2, 'ADD', operator.add)
SUB = Function(2, 'SUB', operator.sub)
MUL = Function(2, 'MUL', operator.mul)
DIV = Function(2, 'DIV', pdiv)
MOD = Function(2, 'MOD', mod)
POW = Function(2, 'POW', math.pow)
EXP = Function(1, 'EXP', math.exp)
SQRT = Function(1, 'SQRT', sqrt)
SIN = Function(1, 'SIN', math.sin)
COS = Function(1, 'COS', math.cos)
LOG2 = Function(1, 'LOG2', log2)
LOG10 = Function(1, 'LOG10', log10)
FLOOR = Function(1, 'FLOOR', math.floor)
CEIL = Function(1, 'CEIL', math.ceil)


# Logical Functions
AND = Function(2, 'AND', lambda x,y : int(x) & int(y))
OR  = Function(2, 'OR', lambda x,y : int(x) | int(y))
NOT = Function(1, 'NOT', lambda x : ~int(x))
NAND = Function(2, 'NAND', lambda x,y : ~(int(x) & int(y)))
NOR = Function(2, 'NOR', lambda x,y : ~(int(x) | int(y)))

# Policy Search / Classification

LT = Function(2, 'LT', lambda x,y : b2f(x < y))
LTE = Function(2, 'LTE', lambda x,y : b2f(x <= y))
GT = Function(2, 'GT', lambda x,y : b2f(x > y))
GTE = Function(2, 'GTE',lambda x,y : b2f(x >= y))
EQ = Function(2, 'EQ', lambda x,y : b2f(x == y))
MIN = Function(2, 'MIN', lambda x,y : min(x,y))
MAX = Function(2, 'MAX', lambda x,y : max(x,y))
NEG = Function(1, 'NEQ', lambda x : operator.neg(x))
IF = Function(3, 'IF', lambda x,y,z : y if f2b(x) else z)
IFLEZ = Function(3, 'IFLEZ', lambda x,y,z : y if x <= 0 else z)
IFGTZ = Function(3, 'IFGTZ', lambda x,y,z : y if x > 0 else z)