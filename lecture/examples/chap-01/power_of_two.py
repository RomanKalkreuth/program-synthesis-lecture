import sys
import time

def verify_inequality_recursive(n: int) -> bool:
    """
    Recursive verification of the statement 2^n > 2 * n
    """
    if n < 3:
        raise ValueError("Statement not defined for n < 3")
    elif n == 3:
        return True
    else:
        p_k = 2 ** n > 2 * n
        return verify_inequality_recursive(n - 1) if p_k else False

def verify_inequality_iterative(n: int) -> bool:
    """
    Iterative verification of the statement 2^n > 2 * n
    """
    p_k1 = None
    a = 3
    p2 = 2**a
    for k1 in range(4, n+1):
        p2 *= 2
        p_k1 = 2 * p2 > 2 * k1
        if not p_k1:
            break
    return p_k1

def verify_inequality_gpt(n_max):
    """
    Function was written by ChatGPT.

    Verifies that 2^n > 2n for all n > 2 and n <= n_max.
    Based on a proof by induction.
    """
    if n_max <= 2:
        print("Please provide n_max > 2")
        return

    # Base case
    base_case_n = 3
    assert 2 ** base_case_n > 2 * base_case_n, f"Base case failed for n={base_case_n}"

    # Inductive step check
    for k in range(base_case_n, n_max):
        left = 2 ** (k + 1)
        right = 2 * (k + 1)
        previous = 2 ** k > 2 * k
        current = left > right
        if not (previous and current):
            return

def measure_runtime(fun: callable, n: int):
    """
    Runtime measurement if multiple runs of the provided function are considered
    """
    measurements = []
    for _ in range(0, 30):
        start = time.time()
        fun(n)
        end = time.time()
        measurements.append(end - start)
    avg = sum(measurements) / len(measurements)
    print(f"Runtime of function {fun.__name__}: {avg}s")

def main():
    sys.setrecursionlimit(10000)
    measure_runtime(verify_inequality_recursive, 8000)
    measure_runtime(verify_inequality_iterative, 8000)
    measure_runtime(verify_inequality_gpt, 8000)

if __name__ == "__main__":
    main()

