import operator
from enum import Enum

from src.benchmark import LSBenchmark
from src.chap03.naive_search import random_walk
from src.chap03.stochastic_search import stochastic_hc
from src.chap03.tree import Node, evaluate_tree
from src.functions import AND, OR, NAND, NOR
from src.problem import BlackBox
from src.loss import Loss
from src.symbol import Var, Const

MAX_DEPTH = 7
MAX_ITER = 10000
NUM_TRIALS = 1
IDEAL = 0

class Algorithm(Enum):
    RANDOM_WALK = 0
    HILL_CLIMBING = 1

X, y = LSBenchmark.truth_table(n=4, objective=LSBenchmark.majority)

non_terminals = [AND, OR, NAND, NOR]
terminals = [Var("x1", 0),
             Var("x2", 1),
             Var("x3", 2),
             Var("x4", 3)]

loss = Loss.hamming_distance
evaluator = evaluate_tree
comparator = operator.le

algorithm = Algorithm.RANDOM_WALK

problem = BlackBox(X_=X,
                   y_=y,
                   loss_=loss,
                   evaluator_=evaluator)
if algorithm == Algorithm.RANDOM_WALK:
    solution = random_walk(problem=problem,
                           non_terminals=non_terminals,
                           terminals=terminals,
                           max_iter=MAX_ITER,
                           num_trials=NUM_TRIALS,
                           comparator=comparator,
                           ideal=IDEAL,
                           max_depth=MAX_DEPTH)
else:
    solution = stochastic_hc(problem=problem,
                         num_neighbours=1,
                         max_iter=MAX_ITER,
                         num_trials=NUM_TRIALS,
                         comparator=comparator,
                         ideal=IDEAL,
                         max_tree_depth=MAX_DEPTH,
                         non_terminals=non_terminals,
                         terminals=terminals,
                         steepest=True,
                         report_iteration=True)

