"""
Problem classes used for examples and exercises chapter 3 and 4.

Introduction to Program Synthesis Course
Chair for AI Methodology (AIM)
Faculty of Computer Science, RWTH Aachen University
"""

import numpy as np


class BlackBox:
    """
    Representation of a black box problem.
    """

    def __init__(self, X_, y_, loss_, evaluator_):
        self.X = X_
        self.y = y_
        self.n = len(X_)
        self.loss = loss_
        self.evaluator = evaluator_

    def evaluate(self, candidate: object, *args):
        predictions = self.predict(candidate, *args)
        return self.cost(predictions)

    def predict(self, candidate: object, *args):
        predictions = []
        for observation in self.X:
            predictions.append(self.predict_observation(candidate, observation, *args))
        return predictions

    def predict_observation(self, candidate, obs, *args):
        return self.evaluator(candidate, obs, *args)

    def cost(self, predictions):
        cost = 0.0
        for idx in range(self.n):
            cost += self.loss(self.y[idx], predictions[idx])
        return cost

class ProgramSynthesis:
    """
    Represent a program synthesis problem where the evaluation is based on a dataset
    that consists of positive examples and counterexamples.
    """

    def __init__(self, dataset_, evaluator_, minimizing_: bool = False):
        self.dataset = dataset_
        self.evaluator = evaluator_
        self.minimizing = minimizing_

    def is_ideal(self, fitness):
        return fitness == len(self.dataset)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def binary_step(self, x, threshold=0.5):
        return 0 if self.sigmoid(x) <= threshold else 1

    def predict_observation(self, candidate, obs, *args):
        return self.evaluator(candidate, obs, *args)

    def evaluate(self, candidate: object, *args):
        predictions = []
        for obs in self.dataset:
            prediction = self.predict_observation(candidate, obs, *args)
            prediction = self.binary_step(prediction)
            predictions.append(prediction)
        result = self.cost(predictions)
        return result

    def cost(self, predictions):
        cost = 0
        for i, prediction in enumerate(predictions):
            cost += 1 if prediction == self.dataset[i][1] else 0
        return cost