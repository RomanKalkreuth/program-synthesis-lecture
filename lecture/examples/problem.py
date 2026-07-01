"""
Problem classes used for examples and exercises chapter 3 and 4.

Introduction to Program Synthesis Course
Chair for AI Methodology (AIM)
Faculty of Computer Science, RWTH Aachen University
"""

class BlackBoxProblem:
    """
    Representation of black box problem.
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
        return self.evaluator(candidate, [obs], *args)

    def cost(self, predictions):
        cost = 0.0
        for idx in range(self.n):
            cost += self.loss(self.y[idx], predictions[idx])
        return cost