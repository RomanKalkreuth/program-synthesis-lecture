from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    symbol: str = None
    annotated: bool = False
    next: Node = None
    prev: Node = None
    nesting: Node = None


def create_node(symbol: str) -> Node:
    return Node(symbol=symbol, annotated=True)


def append_node(tail: Node, symbol: str):
    node = create_node(symbol=symbol)
    tail.next = node
    node.prev = tail


def nest_node(node_ptr: Node, sublist: Node, append: bool):
    if append:
        new_node = create_node("\0")
        node_ptr.next = new_node
        node_ptr = new_node
    node_ptr.nesting = sublist


def tail(head: Node) -> Node:
    node_ptr = head
    while node_ptr.next is not None:
        node_ptr = node_ptr.next
    return node_ptr


def traverse(head: Node, level=0):
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
    node_ptr = head

    while node_ptr is not None:
        if node_ptr.nesting is not None:
            remove_list(node_ptr.nesting)
        tmp = node_ptr.next
        del node_ptr
        node_ptr = tmp


def create_list(expr: list, init_head: bool, idx: int = 0, append_nesting: bool = True):
    head = None
    node_ptr = None

    if init_head:
        head = Node()
        head.annotated = False
        node_ptr = head

    while idx < len(expr):
        s = expr[idx]
        if s != ' ':
            if s == '(':
                idx += 1
                subhead, idx = create_list(expr, init_head=True, idx=idx)
                if head is None:
                    head = subhead
                    node_ptr = head
                else:
                    nest_node(node_ptr, subhead, append_nesting)
                    node_ptr = node_ptr.next
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
