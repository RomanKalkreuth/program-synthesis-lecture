import random
import configuration
from util import arity

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
        node.symbol = configuration.TERMINALS[random.randint(0, len(configuration.TERMINALS) - 1)]
    else:
        node.symbol = configuration.FUNCTIONS[random.randint(0, len(configuration.FUNCTIONS) - 1)]
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
    if tree.symbol in configuration.FUNCTIONS:
        if arity(tree.symbol) == 1:
            return tree.symbol(evaluate_tree(tree.left, input))
        else:
            return tree.symbol(evaluate_tree(tree.left, input), evaluate_tree(tree.right, input))
    elif tree.symbol in configuration.VARIABLES:
        if configuration.NUM_VARIABLES > 1:
            input_index = configuration.VARIABLES.index(tree.symbol)
            return input[input_index]
        else:
            return input
    else:
        return tree.symbol
