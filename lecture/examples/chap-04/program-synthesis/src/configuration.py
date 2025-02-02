from enum import Enum
from src.functions import *

class Algorithm(Enum):
    ONE_PLUS_LAMBDA = 0
    MU_PLUS_LAMBDA = 1

FUNCTIONS = [ADD, SUB, MUL, DIV, LOG10, MOD, FLOOR, CEIL, AND, OR, NAND, NOR, NOT, LT, LTE, GT, GTE, EQ, MIN, MAX, NEG]
TERMINALS = (['x'])
# [0, 1, 2, math.pi, math.e]
VARIABLES = [terminal for terminal in TERMINALS if type(terminal) == str]
NUM_FUNCTIONS = len(FUNCTIONS)
NUM_TERMINALS = len(TERMINALS)
NUM_VARIABLES = len(VARIABLES)
NUM_GENERATIONS = 20000
MIN_TREE_DEPTH = 2
MAX_TREE_DEPTH = 6
SUBTREE_DEPTH = 4
LAMBDA = 8
MU = 16
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.1
ALGORITHM = Algorithm.MU_PLUS_LAMBDA
MINIMIZING = False

@dataclass
class Config:
    num_jobs: int
    max_generations: int
    minimizing: bool
    ideal_fitness: float
    tree_init_depth: tuple
    max_tree_depth: int
    max_size: int
    subtree_depth: int
    functions: list
    terminals: list
    variables: list
    num_functions: int
    num_terminals: int
    num_variables: int
    comparator: operator
    evaluator: callable
    algorithm: callable
    report_interval: int

@dataclass
class Hyperparameters:
    mu: int
    lambda_: int
    crossover_rate: float
    mutation_rate: float