import operator
from enum import Enum

from src.benchmarks.leetcode import power_of_two
from src.chap03.naive_search import random_walk
from src.chap03.stochastic_search import stochastic_hc
from src.chap03.tree import evaluate_tree
from src.functions import AND, OR, NAND, NOR, ADD, SUB, MUL, DIV, NOT, LT, LTE, GT, GTE, EQ, MIN, MAX
from src.problem import ProgramSynthesis
from src.symbol import Var

MAX_DEPTH = 7
MAX_ITER = 10000
NUM_TRIALS = 1

class Algorithm(Enum):
    RANDOM_WALK = 0
    HILL_CLIMBING = 1

X = power_of_two.generate_dataset(n=20, m=300)

ideal = len(X)

non_terminals = [ADD, SUB, MUL, DIV, AND, OR, NAND, NOR, LT, LTE, GT, GTE, EQ, MIN, MAX]
terminals = [Var("x", 0)]
evaluator = evaluate_tree
comparator = operator.ge

algorithm = Algorithm.RANDOM_WALK

problem = ProgramSynthesis(dataset_=X, evaluator_=evaluator)

if algorithm == Algorithm.RANDOM_WALK:
    solution = random_walk(problem=problem,
                           non_terminals=non_terminals,
                           terminals=terminals,
                           max_iter=MAX_ITER,
                           num_trials=NUM_TRIALS,
                           comparator=comparator,
                           ideal=ideal,
                           max_depth=MAX_DEPTH)
else:
    solution = stochastic_hc(problem=problem,
                         num_neighbours=1,
                         max_iter=MAX_ITER,
                         num_trials=NUM_TRIALS,
                         comparator=comparator,
                         ideal=ideal,
                         max_tree_depth=MAX_DEPTH,
                         non_terminals=non_terminals,
                         terminals=terminals,
                         steepest=True,
                         report_iteration=True)

