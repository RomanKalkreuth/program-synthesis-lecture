from src import util
from src.benchmarks.benchmark import LSBenchmark
from src.loss import Loss
from src.tree import *
from src.configuration import *
from src.problems import BlackboxProblem
from src.gp import GeneticProgramming
from src.algorithms import one_plus_lambda

X, y = LSBenchmark.truth_table(n=4, objective=LSBenchmark.majority)

evaluator = evaluate_tree
algorithm = one_plus_lambda
comparator = operator.le
functions = [AND, OR, NOT]
terminals = ['x1', 'x2', 'x3', 'x4']
ideal = 0.01
loss = Loss.mean_squared_error
problem = BlackboxProblem(X, y, loss, evaluator, ideal)
solution = None

config = Config(
    num_jobs=1,
    num_generations=10000,
    minimizing=True,
    ideal_fitness=ideal,
    tree_init_depth=(2, 4),
    max_tree_depth=4,
    max_size=30,
    subtree_depth=4,
    functions=functions,
    terminals=terminals,
    variables=terminals,
    num_functions=len(functions),
    num_terminals=len(terminals),
    num_variables=len(terminals),
    comparator=comparator,
    evaluator =evaluator,
    algorithm=algorithm,
    report_interval=10
)

hyperparameters = Hyperparameters(
    mu=1,
    lambda_=1,
    crossover_rate=0.5,
    mutation_rate=0.1
)


GeneticProgramming.config = config
solution = GeneticProgramming.evolve(algorithm, config, hyperparameters, problem)

expr = util.generate_symbolic_expression(solution)
print(expr)