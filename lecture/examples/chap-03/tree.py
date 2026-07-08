from inspect import signature
from src import symbol

class Node:
    """
    Representation of a tree node used to represent a binary computational tree.
    """

    def __init__(self, symbol_=None, left_=None, right_=None, parent_=None):
        self._symbol = symbol_
        self.left = left_
        self.right = right_
        self.parent = parent_

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    def __call__(self, *args):
        return self._symbol(*args)

    def arity(self):
        return len(signature(self._symbol).parameters)


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