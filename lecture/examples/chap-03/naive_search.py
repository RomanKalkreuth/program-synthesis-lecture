"""
Naive search examples that complement the naive search methods presented in chapter 3.

Introduction to Program Synthesis Course
Chair for AI Methodology (AIM)
Faculty of Computer Science, RWTH Aachen University
"""

import operator
from enum import IntEnum
import numpy as np
from src import symbol
from src.chap03.tree import Node
from src.loss import absolute_error
from src.problem import BlackBoxProblem
from src.symbol import Var, Const, Function


class Algorithm(IntEnum):
    ENUMERATIVE_SEARCH = 0
    RANDOM_WALK = 1


def evaluate_tree(node: Node, input: list, non_terminals: list, terminals: list):
    """
    Evaluator for binary computational tree's.

    :param node: tree node to be evaluated
    :param input: input of the tree
    :param non_terminals: set of non terminal symbols
    :param terminals: set of terminals symbols
    :return:
    """
    if node.symbol in non_terminals:
        if node.arity == 1:
            return node(evaluate_tree(node.left, input, non_terminals, terminals))
        else:
            return node(evaluate_tree(node.left, input, non_terminals, terminals),
                        evaluate_tree(node.right, input, non_terminals, terminals))
    elif node.symbol in terminals:
        if isinstance(node.symbol, symbol.Var):
            idx = node.symbol()
            return input[idx]
        else:
            return node.symbol()


def min_tree(terminals: list) -> Node:
    """
    Returns an minimal tree which has only a terminal symbol as root
    and no child nodes.

    :param terminals: set of terminal symbols
    :return: Node with annotated terminal symbol
    """
    rand_terminal = np.random.choice(terminals)
    return Node(symbol_=rand_terminal)


def sample_tree(max_depth: int, non_terminals: list, terminals: list, node: Node = None, depth: int = 0) -> Node:
    """
    Samples a random tree from a set of terminal and non-terminal symbols w.r.t a maximum depth.

    :param max_depth: maximum depth of the sampled tree
    :param terminals: set of terminal symbols
    :param non_terminals: set of non-terminals symbols
    :param node: node to be created or annotated
    :param depth: current depth of the tree
    :return: root node of the tree
    """
    if node is None:
        node = Node()

    if depth >= max_depth - 1:
        node.symbol = np.random.choice(terminals)
    else:
        node.symbol = np.random.choice(non_terminals)
        node.left = Node()
        node.left.parent = node
        sample_tree(max_depth, non_terminals, terminals, node.left, depth + 1)

        node.right = Node()
        node.right.parent = node
        sample_tree(max_depth, non_terminals, terminals, node.right, depth + 1)

    return node


def enumerative_search(problem: BlackBoxProblem, non_terminals: list, terminals: list, comparator: operator,
                       ideal: float, max_depth: int, depth=0, best=None, root=None, current=None) -> Node:
    """
    Naive enumerative search algorithm that searches for solutions recursively.

    :param problem: problem instance
    :param terminals: set of terminal symbols
    :param non_terminals: set of non-terminal symbols
    :param comparator: comparator operator
    :param ideal: ideal cost value
    :param max_depth: maximum depth
    :return: best solution found so far
    """

    def next(current: Node, non_terminals: list, terminals: list) -> Node:
        current.symbol = np.random.choice(non_terminals)
        current.left = Node(symbol_=np.random.choice(terminals), parent_=current)
        current.right = Node(symbol_=np.random.choice(terminals), parent_=current)
        return current

    if current is None:
        current = min_tree(terminals)
        root = current

    if depth >= max_depth:
        return best
    else:
        cost = problem.evaluate(root)

        if best is None:
            best = (current, cost)

        if comparator(cost, ideal):
            print("Ideal solution found at depth #" + str(depth))
            return current
        elif comparator(cost, best[1]):
            best = (current, cost)

        print("Depth: " + str(depth) + " Cost: " + str(cost))
        nxt = next(current, non_terminals, terminals)
        depth += 1
        enumerative_search(problem, non_terminals, terminals, comparator, ideal, max_depth, depth, best, root, nxt.left)
        enumerative_search(problem, non_terminals, terminals, comparator, ideal, max_depth, depth, best, root,
                           nxt.right)
        return best


def random_walk(problem: BlackBoxProblem, non_terminals: list, terminals: list, max_iter: int, num_trials: int,
                comparator: operator,
                ideal: float,
                max_depth,
                report_iter=True,
                report_trial=True
                ) -> Node:
    """
    Simple random walk algorithm that is performed in an iterative fashion.

    :param problem: problem instance
    :param terminals: set of terminal symbols
    :param non_terminals: set of non-terminal symbols
    :param comparator: comparison operator
    :param ideal: ideal cost value
    :param num_trials: Number of trials
    :param ideal: ideal cost function value
    :param max_depth: maximum depth
    :param report_iter:
    :param report_trial:
    :return: best solution obtained
    """
    best = None
    for trial in range(num_trials):
        for iter in range(max_iter):
            depth = np.random.randint(1, max_depth)
            next = sample_tree(depth, non_terminals, terminals)
            cost = problem.evaluate(next)
            candidate = (next, cost)
            if best is None:
                best = candidate
            if comparator(candidate[1], ideal):
                print("Ideal solution found in Trial #" + str(trial))
                return candidate[0]
            elif comparator(candidate[1], best[1]):
                best = candidate
            if report_iter:
                print("Iteration #" + str(iter) + " Best cost: " + str(best[1]))
        if report_trial:
            print("Trial #" + str(trial) + " - Best cost: " + str(best[1]))
    return best[0]


if __name__ == "__main__":
    MAX_ITER = 10
    NUM_TRIALS = 1
    IDEAL = 0.01
    MAX_DEPTH = 8

    ALGORITHM = Algorithm.RANDOM_WALK

    non_terminals = [Function(func_=operator.add, arity_=2, name_="add"),
                     Function(func_=operator.mul, arity_=2, name_="mul")]
    terminals = [Var("x", 0),
                 Const(name_="one", value=1)]

    f = lambda x: x ** 3 + x ** 2 + x

    X = np.linspace(-10.0, 10.0, 50)
    y = np.array([f(x) for x in X])

    loss = absolute_error
    evaluator = evaluate_tree
    comparator = operator.lt

    problem = BlackBoxProblem(X_=X,
                              y_=y,
                              loss_=loss,
                              evaluator_=evaluator)

    if ALGORITHM == Algorithm.RANDOM_WALK:
        best = random_walk(problem=problem,
                    non_terminals=non_terminals,
                    terminals=terminals,
                    max_iter=MAX_ITER,
                    num_trials=NUM_TRIALS,
                    comparator=comparator,
                    ideal=IDEAL,
                    max_depth=MAX_DEPTH)
    elif ALGORITHM == Algorithm.ENUMERATIVE_SEARCH:
        best = enumerative_search(problem=problem,
                           non_terminals=non_terminals,
                           terminals=terminals,
                           comparator=comparator,
                           ideal=IDEAL,
                           max_depth=MAX_DEPTH
                           )
