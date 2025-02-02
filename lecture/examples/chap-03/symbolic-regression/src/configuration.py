import operator
from enum import Enum
from functions import pdiv

class Algorithm(Enum):
    ENUMERATIVE_SEARCH = 0
    HILL_CLIMBING = 1
    BRANCH_AND_BOUND = 2
    ONE_PLUS_LAMBDA = 3

MAX_RECURSION_DEPTH = 10

FUNCTIONS = [operator.mul, operator.add, operator.sub, pdiv]
TERMINALS = ['x', 1]
VARIABLES = [terminal for terminal in TERMINALS if type(terminal) == str]

NUM_FUNCTIONS = len(FUNCTIONS)
NUM_TERMINALS = len(TERMINALS)
NUM_VARIABLES = len(VARIABLES)

MIN_TREE_DEPTH = 2
MAX_TREE_DEPTH = 3
SUBTREE_DEPTH = 3

ALGORITHM = Algorithm.ONE_PLUS_LAMBDA
