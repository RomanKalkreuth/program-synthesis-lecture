from functions import ADD, SUB, MUL, DIV
from symbols import Const

class Stack:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)
        print(f"Pushed: {value}")

    def pop(self):
        if self.is_empty():
            print("Stack underflow")
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def display(self):
        print("Stack:", self.data[::-1])


c0 = Const(name_ = "c0", value=0)
c1 = Const(name_ = "c1", value=1)

s = Stack()
s.push(ADD.__call__)
s.push(SUB.__call__)
s.push(MUL.__call__)
s.push(DIV.__call__)

s.display()