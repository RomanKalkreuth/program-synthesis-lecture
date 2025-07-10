from src import util
from src.benchmarks.benchmark import SRBenchmark
from src.loss import Loss
from src.tree import *
from src.configuration import *
from src.problems import BlackboxProblem
from src.gp import GeneticProgramming
from src.algorithms import one_plus_lambda

X, y = SRBenchmark.random_set(min=-1.0, max=1.0, n=20,objective=SRBenchmark.koza3, dim=1)

evaluator = evaluate_tree
algorithm = one_plus_lambda
comparator = operator.le
functions = [ADD, SUB, MUL, DIV]
terminals = (['x'])
#terminals += [0, 1, 2, math.pi, math.e]
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