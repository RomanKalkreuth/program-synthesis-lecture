"""
Implementation of the direct "algorithmic" proof
for adding two odd numbers in chapter 01-02.
"""

from dataclasses import dataclass

@dataclass
class Number:
    """
    Number composed of a coefficient, term and constant.
    """
    coefficient: int
    term: int
    constant: int

    def value(self):
        return self.coefficient * self.term + self.constant

    def __str__(self):
        return (f"{self.coefficient} * {self.term} + {self.constant} "
                f"= {self.value()}")

@dataclass
class Odd(Number):
    """
    Odd number defined as 2x + 1
    """
    def __init__(self, value):
        self.coefficient = 2
        self.constant = 1
        self.term = (value - 1) / 2

@dataclass
class Even(Number):
    """
    Even number defined as 2x
    """
    def __init__(self, term):
        self.coefficient = 2
        self.constant = 0
        self.term = term

def add_odds(a: Odd, b: Odd) -> Even:
    """
    Performs the addition algorithm as used in the proof:

    a + b = (2x+1) + (2y+1)
          = 2x + 2y + 2
          = 2(x+y+1)
          = 2n

    :param a: first odd number
    :param b: second odd number
    :return: result of addition, a even number 
    """

    # Calculate (x + y + 1)
    n = a.term + b.term + 1
    return Even(n)


def main():
    a = Odd(3)
    b = Odd(15)
    result = add_odds(a, b)
    print(result)

if __name__ == "__main__":
    main()