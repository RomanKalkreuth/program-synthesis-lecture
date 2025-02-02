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

def mu_plus_lambda(problem, config, hyperparameters):
    offsprings = []
    parents = [random_tree(config.max_tree_depth) for _ in range(hyperparameters.mu)]
    fitness = [problem.evaluate(parent) for parent in parents]
    population = zip(parents,fitness)

    for generation in range(config.num_generations):
        population = sorted(population, key=lambda ind: ind[1], reverse=not config.minimizing)
        parents = population[:hyperparameters.mu]

        best_individual = population[0][0]
        best_fitness = population[0][1]

        offsprings.clear()

        if problem.is_ideal(best_fitness):
            print("Ideal solution found in Iteration #" + str(generation))
            return best_individual

        for _ in range(hyperparameters.lambda_):
            offspring = None

            if random.random() <= hyperparameters.crossover_rate:
                parent1 = parents[random.randint(0, hyperparameters.mu - 1)][0]
                parent2 = parents[random.randint(0, hyperparameters.mu - 1)][0]
                offspring = subtree_crossover(parent1, parent2, hyperparameters.crossover_rate)[0]

            if offspring is None:
                parent = parents[random.randint(0, hyperparameters.mu - 1)][0]
                offspring = copy.deepcopy(parent)
                subtree_mutation(offspring, config.subtree_depth)
            elif random.random() <= hyperparameters.mutation_rate:
                subtree_mutation(offspring, config.subtree_depth)

            if size(offspring) > config.max_size:
                offspring = parents[random.randint(0, hyperparameters.mu - 1)][0]

            fitness = problem.evaluate(offspring)
            offsprings.append((offspring, fitness))

        population = parents + offsprings
        if generation % config.report_interval == 0:
            print("Generation #" + str(generation) + " Best fitness: " + str(best_fitness))
    return best_individual


