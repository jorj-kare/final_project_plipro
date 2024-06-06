# copied and modified from
# https://machinelearningmastery.com/evolution-strategies-from-scratch-in-python/

from numpy import asarray
from numpy import cos
from numpy import pi
from numpy import sqrt
from numpy import argsort
from numpy.random import randn
from numpy.random import seed
import matplotlib.pyplot as plt


def rastrigin(x):
    """
    The Rastrigin function is a common test case for optimization algorithms.
    It has a global minimum at x=0 where it achieves a value of 0.
    """
    A = 10
    return A * len(x) + sum([(xi**2 - A * cos(2 * pi * xi)) for xi in x])


def in_bounds(point, bounds):
    """
    Check if a point is within the bounds of the search.
    Assumes that bounds is a 2D array with shape (n, 2) where n is the number of dimensions.
    """
    # enumerate all dimensions of the point
    for d in range(len(bounds)):
        # check if out of bounds for this dimension
        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
            return False
    return True


def es_comma(objective, bounds, generations, std_dev, mu, lam, initial_mean_np):
    """
    Evolution Strategy (mu, lambda) algorithm.

    Args:
        objective (function): The objective function to be optimized.
        bounds (list): A list of tuples specifying the lower and upper bounds for each variable.
        generations (int): The number of generations to run the algorithm.
        std_dev (float): The standard deviation used for mutation.
        mu (int): The number of parents to select for reproduction.
        lam (int): The total population size.
        initial_mean_np (numpy.ndarray): The initial mean of the population.

    Returns:
        tuple: A tuple containing the best solution found, the corresponding fitness value, and a list of generation means.
    """
    best, best_eval = None, -1e10
    generation_means = list()
    # calculate the number of children per parent
    n_children = int(lam / mu)
    # initial population
    population = list()
    # how much to decay the standard deviation with each generation
    decay_factor = 0.99

    for _ in range(lam):
        while True:
            candidate = initial_mean_np + randn(len(bounds)) * std_dev
            if in_bounds(candidate, bounds):
                break
        population.append(candidate)

    # perform the search
    for generation in range(generations):
        # reduce std_dev by decay_factor
        std_dev *= decay_factor
        # evaluate fitness for the population
        scores = [objective(c) for c in population]
        generation_means.append(sum(scores) / len(scores))
        # rank scores in ascending order and select the top mu ranked solutions
        selected = argsort(scores)[-mu:]
        # create children from parents
        children = list()
        for i in selected:
            # check if this parent is the best solution ever seen
            if scores[i] > best_eval:
                best, best_eval = population[i], scores[i]
                # print('%d, Best: f(%s) = %.5f' % (generation, best, -best_eval))
            # create children for parent
            for _ in range(n_children):
                while True:
                    child = population[i] + randn(len(bounds)) * std_dev
                    if in_bounds(child, bounds):
                        break
                children.append(child)
        # replace population with children
        population = children

    return best, best_eval, generation_means
