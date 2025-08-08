from __future__ import annotations
from dataclasses import dataclass

ELBOW = "└──"
PIPE = "│  "
TEE = "├──"
BLANK = "   "

@dataclass
class Node:
    symbol: str
    annotated: bool = False
    parent: Node = None
    left: Node = None
    right: Node = None

def traverse(tree, term="", left=False, right=False):
    if tree.symbol is None:
        return

    prefix = ""

    if right or tree.parent is None:
        prefix += ELBOW
    elif left and tree.parent.right is None:
        prefix += ELBOW
    elif left:
        prefix += TEE

    print("%s%s%s" % (term, prefix, tree.symbol))

    appendix = (PIPE if left and tree.parent.right is not None else BLANK)

    if tree.left is not None:
        traverse(tree.left, term + appendix, left=True, right=False)
    if tree.right is not None:
        traverse(tree.right, term + appendix, left=False, right=True)

def remove_tree(root: Node):
    if root.left is not None:
        remove_tree(root.left)
    if root.right is not None:
        remove_tree(root.right)
    del root
    return

def append_node(node_ptr, symbol):
    if node_ptr.left is None:
        node_ptr.left = Node(symbol=symbol, annotated=True)
        node_ptr.left.parent = node_ptr
    else:
        node_ptr.right = Node(symbol=symbol, annotated=True)
        node_ptr.right.parent = node_ptr

def create_node(symbol: str) -> Node:
    return Node(symbol=symbol, annotated=True)

def create_tree(expr: list, init_root: bool, idx: int = 0):
    root = None
    node_ptr = None

    if init_root:
        root = Node('')
        root.annotated = False
        node_ptr = root

    while idx < len(expr):
        s = expr[idx]
        if s != ' ':
            if s == '(':
                idx += 1
                subroot, idx = create_tree(expr, init_root=True, idx=idx)
                if root is None:
                    root = subroot
                    node_ptr = root
                else:
                    if node_ptr.left is None:
                        node_ptr.left = subroot
                    else:
                        node_ptr.right = subroot
                    node_ptr.parent = root
            elif s == ')':
                break
            else:
                if not root.annotated:
                    root.symbol = s
                    root.annotated = True
                else:
                    append_node(node_ptr, s)
        idx += 1
    return root, idx

def main():
    expr = "(+ (* a (+ b c)) (* d (/ e f)))"
    symbols = list(expr)
    tree, idx = create_tree(symbols, init_root=False)
    tree.parent = None
    traverse(tree)
    remove_tree(tree)

if __name__ == "__main__":
    main()



