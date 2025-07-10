import random
import copy

from src.operators import subtree_mutation, subtree_crossover
from src.tree import random_tree, size

def one_plus_lambda(problem, config, hyperparameters):

    parent = random_tree(config.max_tree_depth)
    best_fitness = problem.evaluate(parent)

    for generation in range(config.num_generations):
        for _ in range(hyperparameters.lambda_):
            offspring = copy.deepcopy(parent)
            subtree_mutation(offspring, config.subtree_depth)

            if size(offspring) > config.max_size:
                continue

            fitness = problem.evaluate(offspring)

            if config.comparator(fitness, best_fitness):
                parent = offspring
                best_fitness = fitness

            if problem.is_ideal(best_fitness):
                print("Ideal solution found in Iteration #" + str(generation))
                return parent

        if generation % config.report_interval == 0:
            print("Generation #" + str(generation) + " Best fitness: " + str(best_fitness))
    return parent


