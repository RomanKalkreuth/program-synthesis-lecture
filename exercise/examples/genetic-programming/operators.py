import copy
import random
import queue
from src.tree import size, random_tree

def subtree_at(tree, node_num: int):
    q = queue.Queue()
    q.put(tree)
    count = 0

    while not q.empty():
        subtree = q.get()

        if count == node_num:
            return subtree

        count += 1

        if subtree.left is not None:
            q.put(subtree.left)
        if subtree.right is not None:
            q.put(subtree.right)

def replace_subtree(tree, replacement: object, node: int):
    subtree = subtree_at(tree, node)
    subtree.symbol = replacement.symbol
    subtree.left = replacement.left
    subtree.right = replacement.right

def subtree(tree, node_num: int):
    """
    Returns a clone of the subtree at a specified node number.
    """
    subtree = subtree_at(tree, node_num)

    if subtree is None:
        raise RuntimeError('Subtree not found')

    subtree.parent = None

    return copy.deepcopy(subtree)

def subtree_mutation(tree: object, max_depth: int = 6):
    def size(tree, left: int = 0, right: int = 0) -> int:
        if tree.symbol is None:
            return 0
        if tree.left is not None:
            left = size(tree.left)
        if tree.right is not None:
            right = size(tree.right)

        return 1 + left + right

    mutation_point = random.randint(1, size(tree) - 1)
    subtree = random_tree(max_depth)
    replace_subtree(tree, subtree, mutation_point)