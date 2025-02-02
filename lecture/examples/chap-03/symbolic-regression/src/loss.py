import math
import numpy as np

def absolute_error(actual, prediction):
    return np.sum(np.abs(np.subtract(actual, prediction)))


def mean_squared_error(actual, prediction):
    return np.square(np.subtract(actual, prediction)).mean()


def root_mean_squared_error(actual, prediction):
    return math.sqrt(mean_squared_error(actual, prediction))