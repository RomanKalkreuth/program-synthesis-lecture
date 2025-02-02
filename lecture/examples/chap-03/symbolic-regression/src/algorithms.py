import random
import copy
import configuration
from operators import subtree_mutation
from src.tree import evaluate_tree
from tree import Node, random_tree

def sample_neighbour(node):
    if node.symbol in configuration.TERMINALS:
        random_tree(configuration.SUBTREE_DEPTH, node)
    else:
        if node.left is not None:
            sample_neighbour(node.left)
        elif node.right is not None:
            sample_neighbour(node.right)
    return node


def sample_neighbours(node, num_neighbours):
    neighbours = []
    for _ in range(num_neighbours):
        neighbour = sample_neighbour(copy.deepcopy(node))
        neighbours.append(neighbour)
    return neighbours


def replace(current, neighbours, comperator, steepest=False):
    replacements = [neighbour for neighbour in neighbours if comperator(neighbour[1], current[1])]
    if len(replacements) > 1:
        if steepest:
            return sorted(replacements, key=lambda n: n[1])[0]
        else:
            return replacements[random.randint(0, len(replacements)) - 1]
    else:
        return current

def get_bounds(actual):
    return min(actual), max(actual)

def one_plus_lambda(problem, max_gen, trials, lambda_, comparator, ideal, max_tree_depth, subtree_depth, report_iteration = False,
                    report_trial = True):
    evaluator = evaluate_tree
    for trial in range(trials):
        parent = random_tree(max_tree_depth)
        best_fitness = problem.evaluate(parent, evaluator)
        for iteration in range(max_gen):
            for _ in range(lambda_):
                offspring = copy.deepcopy(parent)
                subtree_mutation(offspring, subtree_depth)
                fitness = problem.evaluate(offspring, evaluator)

                if comparator(fitness, best_fitness):
                    parent = offspring
                    best_fitness = fitness

                if comparator(best_fitness, ideal):
                    print("Ideal solution found in Iteration #" + str(iteration))
                    return parent

                if report_iteration:
                    print("Iteration #" + str(iteration) + " Best fitness: " + str(best_fitness))
        if report_trial:
            print("Trial #" + str(trial) + " - Best fitness: " + str(best_fitness))
    return parent


def enumerative_search(problem, current, num_steps, comparator, ideal, depth=0):
    if depth >= configuration.MAX_RECURSION_DEPTH:
        return
    else:
        predictions = problem.predict(problem, current)
        cost = problem.cost(predictions)
        if comparator(cost, ideal):
            print("Ideal solution found at depth #" + str(depth))
            return current

    steps = sample_neighbours(current, num_steps)
    for step in steps:
        s = enumerative_search(problem, step, num_steps, comparator, ideal, depth + 1)
        if s is not None:
            return s

def random_walk(problem, max_iter, num_trials, comparator, ideal, max_tree_depth):
    best = None
    for trial in range(num_trials):
        for iteration in range(max_iter):
            tree = random_tree(max_tree_depth, Node())
            cost = problem.cost(problem.predict(problem, tree))
            candidate = (tree, cost)
            if best is None:
                best = candidate
            if comparator(candidate[1], ideal):
                print("Ideal solution found in Trial #" + str(trial))
                return candidate[0]
            elif comparator(candidate[1], best[1]):
                best = candidate
            print("Iteration #" + str(iteration) + " Best cost: " + str(best[1]))
        print("Trial #" + str(trial) + " - Best cost: " + str(best[1]))


def stochastic_hc(problem, num_neighbours, max_iter, num_trials, comparator, ideal, max_tree_depth, steepest=False, report_iteration = False,
                  report_trial = True):
    neighbours = []
    evaluator = evaluate_tree
    for trial in range(num_trials):
        init_tree = random_tree(max_tree_depth, Node())
        init_cost = problem.evaluate(init_tree, evaluator)
        current = (init_tree, init_cost)
        for iteration in range(max_iter):
            neighbours.clear()
            for count in range(num_neighbours):
                neighbour = sample_neighbour(copy.deepcopy(current[0]))
                cost = problem.evaluate(init_tree, evaluator)
                neighbours.append((neighbour, cost))
            current = replace(current, neighbours, comparator, steepest)
            if comparator(current[1], ideal):
                print("Ideal solution found in Trial #" + str(trial))
                return current[0]
            if report_iteration:
                print("Iteration #" + str(iteration) + " Best cost: " + str(current[1]))
        if report_trial:
            print("Trial #" + str(trial) + " - Best cost: " + str(current[1]))


def branch_and_bound(problem, lower_bound, upper_bound, current, num_neighbours, comparator, ideal, depth=0):
    steps = sample_neighbours(current[0], num_neighbours)
    for step in steps:
        predictions = predict(problem, step)
        bounds = get_bounds(predictions)
        if lower_bound <= bounds[0] and bounds[1] <= upper_bound \
                and depth <= MAX_RECURSION_DEPTH:
            cost = problem.cost(predictions)
            if comparator(cost, ideal):
                print("Ideal solution found at depth #" + str(depth))
                return step
            elif branch_and_bound(problem, lower_bound, upper_bound, (step, cost),
                                  num_neighbours, comparator, ideal, depth + 1):
                return True
    return False