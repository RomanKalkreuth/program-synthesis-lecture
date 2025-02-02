from src import util
from src.tree import *
from src.configuration import *
import src.benchmarks.leetcode.power_of_two as power_of_two
from src.problems import SynthesisProblem
from src.gp import GeneticProgramming
from src.algorithms import one_plus_lambda

training_data = power_of_two.generate_dataset(n=20, m=300)

evaluator = evaluate_tree
functions = [ADD, SUB, MUL, DIV, LOG10, MOD, FLOOR, CEIL, AND, OR, NAND, NOR, NOT, LT, LTE, GT, GTE, EQ, MIN, MAX, NEG]
terminals = (['x'])
#terminals += [0, 1, 2, math.pi, math.e]
comparator = operator.ge
algorithm = one_plus_lambda
ideal = len(training_data)
problem = SynthesisProblem(dataset_=training_data, evaluator_=evaluator)
solution = None

config = Config(
    num_jobs=1,
    num_generations=10000,
    minimizing=False,
    ideal_fitness=100,
    tree_init_depth=(2, 4),
    max_tree_depth=6,
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
    algorithm=Algorithm.MU_PLUS_LAMBDA,
    report_interval=10
)

hyperparameters = Hyperparameters(
    mu=8,
    lambda_=128,
    crossover_rate=0.5,
    mutation_rate=0.1
)

GeneticProgramming.config = config
solution = GeneticProgramming.evolve(algorithm, config, hyperparameters, problem)

expr = util.generate_symbolic_expression(solution)
print(expr)
