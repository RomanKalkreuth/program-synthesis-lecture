import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from src.algorithms import one_plus_lambda
from src.configuration import Config, Hyperparameters, Algorithm
from src.gp import GeneticProgramming
from src.tree import *
from src.problems import *
from src.functions import *
from src.util import get_variables_from_terminals

env = gym.make('CartPole-v1')
wrapped_env = FlattenObservation(env)
NUM_INPUTS = wrapped_env.observation_space.shape[0]

evaluator = evaluate_tree
comparator = operator.ge
problem = PolicySearch(env=env, ideal_=100, evaluator_=evaluator)
functions = [ADD, SUB, MUL, DIV, LOG10, MOD, FLOOR, CEIL, AND, OR,
             NAND, NOR, NOT, LT, LTE, GT, GTE, EQ, MIN, MAX, NEG]
terminals = ["x" + str(i) for i in range(NUM_INPUTS)]
terminals += [0, 1, 2, math.pi, math.e]
variables = get_variables_from_terminals(terminals)
algorithm = one_plus_lambda
ideal = 500
solution = None

config = Config(
    num_jobs=1,
    num_generations=10000,
    minimizing=False,
    ideal_fitness=500,
    tree_init_depth=(2, 4),
    max_tree_depth=6,
    max_size=30,
    subtree_depth=4,
    functions=functions,
    terminals=terminals,
    variables=variables,
    num_functions=len(functions),
    num_terminals=len(terminals),
    num_variables=len(variables),
    comparator=comparator,
    evaluator = evaluator,
    algorithm=Algorithm.MU_PLUS_LAMBDA,
    report_interval=1
)

hyperparameters = Hyperparameters(
    mu=10,
    lambda_=10,
    crossover_rate=0.7,
    mutation_rate=0.05
)

GeneticProgramming.config = config
#GeneticProgramming.evolve(algorithm, config, hyperparameters, problem)
