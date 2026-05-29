"""
Simple example of a nested list addressed in chapter 2.1
(program representation/tree)

Introduction to Program Synthesis Course
Chair for AI Methodology (AIM)
Faculty of Computer Science, RWTH Aachen University
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    """
    Representation of a node that
    is specified with an annotation (symbol) and the
    linkage to neighborhood nodes as well as listings.
    """
    symbol: str = None
    annotated: bool = False
    next: Node = None
    prev: Node = None
    nesting: Node = None


def create_node(symbol: str) -> Node:
    """
    Creates a new node and annotates it with the given symbol.

    :param symbol: symbol to be annotated
    :return: newly created node
    """
    return Node(symbol=symbol, annotated=True)


def append_node(tail: Node, symbol: str):
    """
    Create and append a new node to the tail of the list annotated
    with the given symbol.

    :param tail: tail node of the list
    :param symbol: symbol to be annotated
    """
    node = create_node(symbol=symbol)
    tail.next = node
    node.prev = tail


def nest_node(node_ptr: Node, sublist: Node, append: bool):
    """
    Create a new sublist nesting on a referenced node.

    :param node_ptr: Reference to the node to be nested
    :param sublist: Sublist to be nested
    :param append: append a new node that only serves as a nesting reference
    """
    if append:
        # Annotated the node to append with the termination symbol
        new_node = create_node("\0")
        node_ptr.next = new_node
        node_ptr = new_node
    node_ptr.nesting = sublist


def tail(head: Node) -> Node:
    """
    Iterate the list and return the tail node.

    :param head: head node of the list
    :return: tail node
    """
    node_ptr = head
    while node_ptr.next is not None:
        node_ptr = node_ptr.next
    return node_ptr


def traverse(head: Node, level=0):
    """
    Traverses the list recursively and prints the annotations
    of the visited nodes.

    :param head: head of the list
    :param level: current level, zero by default
    """
    node_ptr = head
    space = '\t' * (level) if level > 0 else ''
    print(space, end="")
    while node_ptr is not None:
        print(node_ptr.symbol, end=" ")
        if node_ptr.nesting is not None:
            print("")
            traverse(node_ptr.nesting, level=level + 1)
        node_ptr = node_ptr.next


def remove_list(head: Node):
    """
    Remove the list recursively.
    :param head: head of the list
    """
    node_ptr = head

    while node_ptr is not None:
        if node_ptr.nesting is not None:
            remove_list(node_ptr.nesting)
        tmp = node_ptr.next
        del node_ptr
        node_ptr = tmp


def create_list(expr: list, init_head: bool, idx: int = 0, append_nesting: bool = True):
    """
    Creates a new nested list recursively based on the given (symbolic) expression.

    :param expr: symbolic expression
    :param init_head: option to init the head node
    :param idx: current node index for the recursion
    :param append_nesting: append option for nestings
    """
    head = None
    node_ptr = None

    if init_head:
        head = Node()
        head.annotated = False
        node_ptr = head


    # Iterate over the expression
    n = len(expr)
    while idx < n:
        s = expr[idx]
        if s != ' ':
            # Identify the start of a new sublist
            if s == '(':
                idx += 1
                subhead, idx = create_list(expr, init_head=True, idx=idx)
                # Initialize the global header, if this has not already been done
                if head is None:
                    head = subhead
                    node_ptr = head
                # Otherwise nest the head of the created sublist
                else:
                    nest_node(node_ptr, subhead, append_nesting)
                    node_ptr = node_ptr.next
            # Leave the nesting recursion level
            elif s == ')':
                break
            else:
                if not head.annotated:
                    head.symbol = s
                    head.annotated = True
                else:
                    append_node(node_ptr, s)
                    node_ptr = node_ptr.next
        idx += 1
    return head, idx


def main():
    expr = "(+ (* a (+ b c)) (* d (/ e f)))"
    symbols = list(expr)
    head, idx = create_list(symbols, False)
    traverse(head)


if __name__ == "__main__":
    main()
