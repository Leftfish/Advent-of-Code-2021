from statistics import mean, median
from typing import Callable, List

print('Day 7 of Advent of Code!')


def sum_range(a: int, b: int) -> int:
    n = abs(b - a)
    return int(n * (n + 1) / 2)


def move_crabs(crabs: List[int], pos: int, cost_counter: Callable[[int, int], int]) -> int:
    return sum(cost_counter(crab, pos) for crab in crabs)


def crabs_naive(crabs: List[int], cost_counter: Callable[[int, int], int]) -> int:
    minimum = None
    for pos in range(crabs[-1]):
        cost = move_crabs(crabs, pos, cost_counter)
        if not minimum or cost < minimum:
            minimum = cost
    return minimum


def crabs_by_median(crabs: List[int]) -> int:
    median_position = int(median(crabs))
    return sum(abs(median_position - crab) for crab in crabs)


def crabs_by_mean(crabs: List[int]) -> int:
    mean_position = round(mean(crabs))
    costs = []
    for modifier in (-1, 0, 1):
        costs.append(sum(sum_range(crab, mean_position + modifier) for crab in crabs))
    return min(costs)

raw_data = '''16,1,2,0,4,2,7,1,2,14'''

print('Tests...')
crabs = sorted(list(map(int, raw_data.split(','))))
print('Cheap crabs:', crabs_naive(crabs, lambda a, b: abs(b - a)) == 37)
print('Cheap crabs (non naive):', crabs_by_median(crabs) == 37)
print('Expensive crabs:', crabs_naive(crabs, sum_range) == 168)
print('Expensive crabs (non naive):', crabs_by_mean(crabs) == 168)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    crabs = sorted(list(map(int, raw_data.split(','))))
    print('Cheap crabs:', crabs_naive(crabs, lambda a, b: abs(b - a)))
    print('Cheap crabs (non naive):', crabs_by_median(crabs))
    print('Expensive crabs:', crabs_naive(crabs, sum_range))
    print('Expensive crabs (non naive):', crabs_by_mean(crabs))
