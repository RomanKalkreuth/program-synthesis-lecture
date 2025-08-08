import operator
from abc import ABC
from dataclasses import dataclass
from symbols import Function, Terminal

@dataclass
class GPHyperparameters:
    mu: int
    lambda_: int
    strict_selection: bool = False

@dataclass
class GPConfig:
    num_jobs: int
    num_generations: int
    minimizing: bool
    ideal_fitness: float
    comparator: operator
    algorithm: callable
    report_interval: int
    silent_algorithm: bool
    silent_evolver: bool


@dataclass
class Config(ABC):
    non_terminals: list[Function]
    terminals: list[Terminal]
    operators: list

    def __post_init__(self):
        self.num_functions = len(self.non_terminals)
        self.num_terminals = len(self.terminals)

        arities = [function.arity for function in self.non_terminals]
        self.min_arity = min(arities)
        self.max_arity = max(arities)


@dataclass
class GraphConfig(Config):
    min_nodes: int
    max_nodes: int
    num_inputs: int
    num_outputs: int
    symbol_ratio = 0.5
    min_arity: int = None
    max_arity: int = None

@dataclass
class TreeConfig(Config):
    min_init_depth: int
    max_init_depth: int
    max_size: int
    subtree_depth: int
    arity: int

