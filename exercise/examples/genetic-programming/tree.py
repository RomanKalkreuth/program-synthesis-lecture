import random
from src.util import *
from src.gp import GeneticProgramming as gp

class Node:
    def __init__(self, symbol=None, left=None, right=None, parent=None):
        self.symbol = symbol
        self.left = left
        self.right = right
        self.parent = parent

    def get_symbol(self) -> str:
        return str(self.symbol)


def size(node, left: int = 0, right: int = 0) -> int:
    """
    Recursively determines the size of a tree which is defined as the number of nodes.
    """
    if node.symbol is None:
        return 0

    if node.left is not None:
        left = size(node.left)
    if node.right is not None:
        right = size(node.right)

    return 1 + left + right


def random_tree(max_depth: int, node=None, depth: int = 0):
    if node is None:
        node = Node()

    if depth >= max_depth - 1:
        node.symbol = gp.config.terminals[random.randint(0, gp.config.num_terminals - 1 )]
    else:
        node.symbol = gp.config.functions[random.randint(0, gp.config.num_functions - 1 )]
        node.left = Node()
        node.left.parent = node
        random_tree(max_depth, node.left, depth + 1)

        if arity(node.symbol) > 1:
            node.right = Node()
            node.right.parent = node
            random_tree(max_depth, node.right, depth + 1)
        else:
            node.right = None
    return node


def evaluate_tree(tree, input: list):
    if tree.symbol in gp.config.functions:
        if arity(tree.symbol) == 1:
            return tree.symbol.call([evaluate_tree(tree.left, input)])
        else:
            return tree.symbol.call([evaluate_tree(tree.left, input), evaluate_tree(tree.right, input)])
    elif tree.symbol in gp.config.variables:
        if gp.config.num_variables > 1:
            input_index = gp.config.variables.index(tree.symbol)
            return input[input_index]
        else:
            return input
    else:
        return tree.symbol
