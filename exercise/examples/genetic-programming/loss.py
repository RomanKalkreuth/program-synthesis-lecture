import math
import numpy as np


class Loss:

    @staticmethod
    def absolute_error(target, prediction):
        return np.sum(np.abs(np.subtract(target, prediction)))

    @staticmethod
    def mean_squared_error(target, prediction):
        return np.square(np.subtract(target, prediction)).mean()

    @staticmethod
    def root_mean_squared_error(target, prediction):
        return math.sqrt(Loss.mean_squared_error(target, prediction))

    @staticmethod
    def hamming_distance(target, prediction):
        return 1 if target != prediction else 0