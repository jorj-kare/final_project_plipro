# copied and modified from
# https://machinelearningmastery.com/evolution-strategies-from-scratch-in-python/

# evolution strategy (mu, lambda) of the rastrigin objective function
from numpy import asarray
from numpy import cos
from numpy import pi
from numpy import sqrt
from numpy import argsort
from numpy.random import randn
from numpy.random import seed
import matplotlib.pyplot as plt


def rastrigin(x):
    A = 10
    return A * len(x) + sum([(xi**2 - A * cos(2 * pi * xi)) for xi in x])


# modifies the Rastrigin function
def objective(x):
    # sign flip - to have a global maximum (instead of a global minimum).
    return -rastrigin(x)


# check if a point is within the bounds of the search
def in_bounds(point, bounds):
    # enumerate all dimensions of the point
    for d in range(len(bounds)):
        # check if out of bounds for this dimension
        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
            return False
    return True


# evolution strategy (mu, lambda) algorithm
def es_comma(
    objective, bounds, generations, std_dev, mu, lam, initial_mean_np
):
    best, best_eval = None, 1e10
    generation_means = list()
    # calculate the number of children per parent
    n_children = int(lam / mu)
    # initial population
    population = list()
    # how much to decay the standard deviation with each generation
    decay_factor=0.99

    for _ in range(lam):
        candidate = None
        while candidate is None or not in_bounds(candidate, bounds):
            candidate = initial_mean_np + randn(len(bounds)) * std_dev
        population.append(candidate)

    # perform the search
    for generation in range(generations):
        # reduce std_dev by decay_factor
        std_dev *= decay_factor
        # evaluate fitness for the population
        scores = [objective(c) for c in population]
        generation_means.append(-sum(scores) / len(scores))
        # rank scores in ascending order and select the top mu ranked solutions
        selected = argsort(scores)[:mu]
        # create children from parents
        children = list()
        for i in selected:
            # check if this parent is the best solution ever seen
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]
                # print('%d, Best: f(%s) = %.5f' % (generation, best, -best_eval))
            # create children for parent
            for _ in range(n_children):
                child = None
                while child is None or not in_bounds(child, bounds):
                    child = population[i] + randn(len(bounds)) * std_dev
                children.append(child)
        # replace population with children
        population = children

    return best, best_eval, generation_means


# # seed the pseudorandom number generator
# seed(1)

# # define the maximum step size
# # Αρχική τιμής της διασποράς της κατανομής.
# # ! changed name
# variance = 1
# std_dev = sqrt(variance)

# # Μέγεθος Πληθυσμού. # number of parents selected
# lam = 100

# # Αριθμός των καλύτερων μελών για ανανέωση της κατανομής.
# # the number of children generated by parents
# mu = 20

# # Αριθμός γενιών (generations).
# generations = 5000

# # Την διαστασιμότητα που επιθυμεί να λύσει το πρόβλημα.
# # Ανάλογα με την διαστασιμότητα, θα πρέπει να αλλάζουν και
# # τα πεδία για αρχικοποίηση της μέσης τιμής.
# dimensions = 2

# # ! changed name from spread to lower_bound and upper_bound
# lower_bound = -5.12
# upper_bound = 5.12
# # define range for input
# bounds = asarray([[lower_bound, upper_bound] for _ in range(dimensions)])
# # print(bounds)

# # Αρχική τιμής της μέσης τιμής της κατανομής:
# # είτε τυχαία επιλογή ανάμεσα σε ένα εύρος είτε σε συγκεκριμένη τιμή.
# # initial_mean = [0] * dimensions
# initial_mean_np = asarray(initial_mean)
# # print(initial_mean_np)

# # θα οπτικοποιεί τα αποτελέσματα και τα βήματα του αλγορίθμου.
# # Πιο συγκεκριμένα, θέλουμε μέσω της γραφικής διεπαφής να δημιουργείται μία
# # γραφική παράσταση όπου ο άξονας χ θα έχει τον αριθμό των γενεών και ο
# # άξονας ψ την μέση τιμή της αντικειμενικής συνάρτησης για τον πληθυσμό ανά γενιά.
# # perform the evolution strategy (mu, lambda) search
# best, score, generation_means = es_comma(
#     objective, bounds, generations, std_dev, mu, lam, initial_mean_np
# )
# print("f(%s) = %f" % (best, -score))
# plt.plot(generation_means)
# plt.show()
