from abc import ABC
from dataclasses import dataclass
from typing import Any

@dataclass
class Symbol(ABC):
    name: str
    type: str
    symbol: callable
    arity: int = None

    def __init__(self, name_):
        self.name = name_
        self.type = self.__class__.__name__

    def __str__(self):
        return str(self.name) + " (" + str(self.type) + ")"

@dataclass
class Function(Symbol):
    def __init__(self, arity_, name_, function_):
        Symbol.__init__(self, name_)
        self.symbol = function_
        self.arity = arity_

    def __call__(self, *args) -> Any:
        assert (len(args) == self.arity)
        return self.symbol(*args)

@dataclass
class Terminal(Symbol):
    def __init__(self, name_, return_):
        Symbol.__init__(self, name_)
        self.symbol = return_

    def __call__(self) -> Any:
        return self.symbol()

@dataclass
class Var(Terminal):
    def __init__(self, name_, index):
        assert (index is not None)
        Terminal.__init__(self, name_, lambda: index)

@dataclass
class Const(Terminal):
    def __init__(self, name_, value):
        assert (value is not None)
        Terminal.__init__(self, name_, lambda: value)

