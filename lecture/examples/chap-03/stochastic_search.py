import copy
import operator
import random
import numpy as np

from src.benchmark import SRBenchmark
from src.chap03.tree import Node, evaluate_tree
from src.functions import ADD, SUB, MUL
from src.problem import BlackBox
from src.loss import Loss
from src.symbol import Var, Const


def replace(current, neighbours, comperator, steepest=False):
    replacements = [neighbour for neighbour in neighbours if comperator(neighbour[1], current[1])]
    if len(replacements) > 1:
        if steepest:
            return sorted(replacements, key=lambda n: n[1])[0]
        else:
            return replacements[random.randint(0, len(replacements)) - 1]
    else:
        return current


def sample_neighbour(node, non_terminals: list, terminals: list):
    if node.symbol in terminals:
        sample_tree
    else:
        if node.left is not None:
            sample_neighbour(node.left, non_terminals, terminals)
        elif node.right is not None:
            sample_neighbour(node.right, non_terminals, terminals)
    return node


def sample_neighbours(node, num_neighbours):
    neighbours = []
    for _ in range(num_neighbours):
        neighbour = sample_neighbour(copy.deepcopy(node))
        neighbours.append(neighbour)
    return neighbours


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


def stochastic_hc(problem, num_neighbours, max_iter, num_trials, comparator, ideal, max_tree_depth,
                  non_terminals: list, terminals: list, steepest=False,
                  report_iteration=False,
                  report_trial=True,
                  report_interval=100):
    neighbours = []
    for trial in range(num_trials):
        init_tree = sample_tree(max_tree_depth, non_terminals, terminals, Node())
        init_cost = problem.evaluate(init_tree, non_terminals, terminals)
        current = (init_tree, init_cost)
        for iter in range(max_iter):
            neighbours.clear()
            for count in range(num_neighbours):
                neighbour = sample_neighbour(copy.deepcopy(current[0]), non_terminals, terminals)
                cost = problem.evaluate(neighbour, non_terminals, terminals)
                neighbours.append((neighbour, cost))
            current = replace(current, neighbours, comparator, steepest)
            if comparator(current[1], ideal):
                print("Ideal solution found in Trial #" + str(trial))
                return current[0]
            if report_iteration:
                if iter % report_interval == 0:
                    print("Iteration #" + str(iter) + " Best cost: " + str(current[1]))
        if report_trial:
            print("Trial #" + str(trial) + " - Best cost: " + str(current[1]))


if __name__ == "__main__":
    MAX_DEPTH = 5

    X, y = SRBenchmark.random_set(min=-1.0, max=1.0, n=20, objective=SRBenchmark.koza1, dim=1)

    non_terminals = [ADD, MUL, SUB]
    terminals = [Var("x", 0),
                 Const(name_="one", value=1)]
    ideal = 0.01
    loss = Loss.mean_squared_error
    evaluator = evaluate_tree
    comparator = operator.le

    problem = BlackBox(X_=X,
                       y_=y,
                       loss_=loss,
                       evaluator_=evaluator)

    solution = stochastic_hc(problem=problem,
                             num_neighbours=1,
                             max_iter=10000,
                             num_trials=10,
                             comparator=comparator,
                             ideal=ideal,
                             max_tree_depth=MAX_DEPTH,
                             non_terminals=non_terminals,
                             terminals=terminals,
                             steepest=True,
                             report_iteration=True)
