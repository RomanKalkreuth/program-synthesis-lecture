"""
Benchmark function used for symbolic regression in chapter 3.

Introduction to Program Synthesis Course
Chair for AI Methodology (AIM)
Faculty of Computer Science, RWTH Aachen University
"""

import numpy as np

def quadratic(x):
    return pow(x, 2) + x

def cubic(x):
    return pow(x, 3) + pow(x, 2) + x

def quartic(x):
    return pow(x, 4) + pow(x, 3) + pow(x, 2) + x

def quintic(x):
    return pow(x, 5) - 2 * pow(x, 3) + x

def sextic(x):
    return pow(x, 6) - 2 * pow(x, 4) + pow(x, 2)

def dataset_uniform(min: float, max: float, n: int, objective: callable, dim=1) -> tuple:
    """
    Generates a dataset by sampling uniformly distributed values and calculating the actual values
    with the given objective function.

    :param min: minimum boundary
    :param max: maximum boundary
    :param n: number of samples
    :param objective: objective function
    :param dim: feature dimension

    :return: tuple of lists that contains the samples and actual values
    """
    def random_samples(min, max, n, dim=1):
        assert min < max
        samples = []

        for i in range(0, dim):
            sample = (max - min) * np.random.random_sample(n) + min
            samples.append(sample)

        return np.stack(samples, axis=1)

    samples = random_samples(min, max, n, dim)
    actuals = [objective(point) for point in samples]

    return samples, actuals

if __name__ == "__main":
    samples, actual = dataset_uniform(min=-1.0,
                                      max=1.0,
                                      n=20,
                                      objective=quartic,
                                      dim=1)