from itertools import product
from random import sample


def permutate(bounds: list, query: str):
    potential_plans = []
    perm_bounds = list(product(*bounds))

    for b in perm_bounds:
        potential_plans.append(query % tuple(map(float, b)))

    if len(potential_plans) > 100:
        return sample(potential_plans, 100)

    return potential_plans
