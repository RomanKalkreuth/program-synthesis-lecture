import numpy as np
import operator as operator
import configuration
import util as util
import algorithms as algorithms
from tree import Node,evaluate_tree
from loss import mean_squared_error

class RegressionProblem:

    def __init__(self, X_, y_, loss_):
        self.X = X_
        self.y = y_
        self.n = len(X_)
        self.loss = loss_

    def evaluate(self, candidate, evaluator):
        predictions = self.predict(candidate, evaluator)
        return self.cost(predictions)

    def predict(self, candidate, evaluator):
        predictions = []
        for observation in self.X:
            predictions.append(self.predict_obs(candidate, evaluator, observation[0]))
        return predictions

    def predict_obs(self, candidate, evaluator, obs):
        return evaluator(candidate, obs)

    def cost(self, predictions):
        cost = 0.0
        for index in range(self.n):
            cost += self.loss(self.y[index], predictions[index])
        return cost


def quadratic(x):
    return x ** 2 + x


def cubic(x):
    return x ** 3 + x ** 2 + x


def quartic(x):
    return x ** 4 + x ** 3 + x ** 2 + x


def dataset_uniform(min, max, n, objective, dim=1):
    def random_samples(min, max, n, dim=1):
        assert min < max
        samples = []

        for i in range(0, dim):
            sample = (max - min) * np.random.random_sample(n) + min
            samples.append(sample)

        return np.stack(samples, axis=1)

    samples = random_samples(min, max, n, dim)
    values = [objective(point) for point in samples]

    return samples, values

def output(solution, problem, evaluator):
    if solution is not False and solution is not None:
        predictions = problem.predict(solution, evaluator)
        util.plot_xy(samples, predictions)
        util.print_tree_vertically(solution)

samples, actual = dataset_uniform(min = -1.0,
                                  max = 1.0,
                                  n = 20,
                                  objective = quartic,
                                  dim=1)


problem = RegressionProblem(samples, actual, mean_squared_error)
evaluator = evaluate_tree
solution = None

if configuration.ALGORITHM == configuration.Algorithm.HILL_CLIMBING:
    solution = algorithms.stochastic_hc(problem =  problem,
                                        num_neighbours= 4,
                                        max_iter = 100,
                                        num_trials= 100,
                                        comparator= operator.lt,
                                        ideal = 0.1,
                                        max_tree_depth=configuration.MAX_TREE_DEPTH,
                                        steepest=False)
elif configuration.ALGORITHM == configuration.Algorithm.ENUMERATIVE_SEARCH:
    init_tree = Node(configuration.TERMINALS[0])
    solution = algorithms.enumerative_search(problem = problem,
                                             current = init_tree,
                                             num_steps = 4,
                                             comparator = operator.lt,
                                             ideal = 0.1)
elif configuration.ALGORITHM == configuration.Algorithm.ONE_PLUS_LAMBDA:
    solution = algorithms.one_plus_lambda(problem=problem,
                                          max_gen=100,
                                          trials = 100,
                                          lambda_=1,
                                          comparator=operator.lt,
                                          ideal=0.1,
                                          max_tree_depth=configuration.MAX_TREE_DEPTH,
                                          subtree_depth=configuration.SUBTREE_DEPTH)

output(solution, problem, evaluator)

