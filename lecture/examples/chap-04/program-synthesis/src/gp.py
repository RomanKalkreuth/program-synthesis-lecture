from src.configuration import Config
from src.problems import Problem

class GeneticProgramming:
    config: Config
    problem: Problem
    algorithm: callable

    @staticmethod
    def init(problem, algorithm, config):
        GeneticProgramming.config = config
        GeneticProgramming.problem = problem
        GeneticProgramming.algorithm = algorithm

    @staticmethod
    def evolve(algorithm, config, hyperparameters, problem):
        return algorithm(problem, config, hyperparameters)
