import gymnasium as gym
import numpy as np
from abc import ABC, abstractmethod
from gymnasium.wrappers import FlattenObservation
import statistics

class GPAgent:
    """
    Agent class that is placed in reinforcement learning environments.
    """

    def __init__(self, env_: gym.Env, flatten_obs = True):
        """
        :param env_: Environment
        :param flatten_obs: Option to flatten the obversation
        """
        self.env = env_
        if flatten_obs:
            self.wrapped_env = FlattenObservation(self.env)

    def evaluate_policy(self, policy, problem, num_episodes = 100, wait_key=False):
        """
        Evaluates a policy in an environment with the selected number of episodes.

        :param policy: Candidate policy from the GP model
        :param num_episodes: Number of episodes
        :param wait_key: Wait key option to see the end result of an episode

        :return: Mean of cumulative rewards
        """
        rewards = []
        for episode in range(num_episodes):
            obs, info = self.env.reset()
            done = False
            cumulative_reward = 0
            while not done:
                if self.wrapped_env is not None:
                    obs_ = self.wrapped_env.observation(obs)
                else:
                    obs_ = obs
                action = self.get_action(policy, problem, obs_)
                next_obs, reward, terminated, truncated, info = self.env.step(action)
                done = terminated or truncated
                obs = next_obs
                cumulative_reward += reward
            if wait_key:
                input("Press Enter to continue...")
            rewards.append(cumulative_reward)
        return statistics.mean(rewards)

    def get_action(self, policy: list[int], problem, obs):
        """
        Predicts the action of an agent equipped with a candidate policy based
        on the given observation.

        :param policy: candidate policy
        :param obs: observation
        :return:
        """
        return problem.predict(policy, obs)

class Problem(ABC):
    ideal: float

    @abstractmethod
    def is_ideal(self, fitness):
        pass

    def binary_step(self, x, threshold=0.5):
        def sigmoid(x):
            return 1 / (1 + np.exp(-1.0 * x))
        return 0 if sigmoid(x) <= threshold else 1

class SynthesisProblem(Problem):
    dataset: list
    evaluator: callable

    def __init__(self, dataset_, evaluator_):
        self.dataset = dataset_
        self.evaluator = evaluator_

    def is_ideal(self, fitness):
        return fitness == len(self.dataset)

    def evaluate(self, candidate):
        predictions = self.predict(candidate)
        return self.cost(predictions)

    def predict(self, candidate):
        predictions = []
        for observation in self.dataset:
            predictions.append(self.predict_obs(candidate, observation[0]))
        return predictions

    def predict_obs(self, candidate, obs):
        return self.binary_step(self.evaluator(candidate, obs))

    def cost(self, predictions):
        cost = 0
        for i, observation in enumerate(self.dataset):
            prediction = predictions[i]
            cost += (1 if observation[1] == prediction else 0)
        return cost


class PolicySearch(SynthesisProblem):
    '''
    A reinforcement learning problem where the fitness is calculated by the
    average reward of the policy.
    '''
    agent: GPAgent
    num_episodes: int

    def __init__(self, env: gym.Env, evaluator_, ideal_,  num_episodes_: int = 100):
        self.agent = GPAgent(env)
        self.ideal = ideal_
        self.num_episodes = num_episodes_
        self.evaluator = evaluator_

    def is_ideal(self, fitness):
        return fitness == self.ideal

    def evaluate(self, genome, num_episodes: int = None, wait_key: bool = False) -> float:
        if num_episodes is None:
            num_episodes = self.num_episodes
        return self.agent.evaluate_policy(genome, self)

    def predict(self, candidate, observation):
        return self.binary_step(self.evaluator(candidate, observation))