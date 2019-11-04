import numpy as np
from sklearn.ensemble import ExtraTreesRegressor

from mushroom.algorithms.value import DoubleFQI, FQI
from mushroom.core import Core
from mushroom.environments import *
from mushroom.policy import EpsGreedy
from mushroom.utils.dataset import compute_J
from mushroom.utils.parameters import Parameter


def learn(alg, alg_params):
    mdp = CarOnHill()
    np.random.seed(1)

    # Policy
    epsilon = Parameter(value=1.)
    pi = EpsGreedy(epsilon=epsilon)

    # Approximator
    approximator_params = dict(input_shape=mdp.info.observation_space.shape,
                               n_actions=mdp.info.action_space.n,
                               n_estimators=50,
                               min_samples_split=5,
                               min_samples_leaf=2)
    approximator = ExtraTreesRegressor

    # Agent
    agent = alg(approximator, pi, mdp.info,
                approximator_params=approximator_params, **alg_params)

    # Algorithm
    core = Core(agent, mdp)

    # Train
    core.learn(n_episodes=5, n_episodes_per_fit=5)

    test_epsilon = Parameter(0.75)
    agent.policy.set_epsilon(test_epsilon)
    dataset = core.evaluate(n_episodes=2)

    return np.mean(compute_J(dataset, mdp.info.gamma))


def test_fqi():
    params = dict(n_iterations=10)
    j = learn(FQI, params)
    j_test = -0.0874123073618985

    assert j == j_test


def test_fqi_boosted():
    params = dict(n_iterations=10, boosted=True)
    j = learn(FQI, params)
    j_test = -0.09201295511778791

    assert j == j_test


def test_double_fqi():
    params = dict(n_iterations=10)
    j = learn(DoubleFQI, params)
    j_test = -0.19933233708925654

    assert j == j_test
