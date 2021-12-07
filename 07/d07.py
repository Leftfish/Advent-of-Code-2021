print('Day 7 of Advent of Code!')

def sum_range(a, b):
    n = abs(b - a)
    return n * (n + 1) / 2

def move_crabs(crabs, pos, cost_counter):
    return sum(cost_counter(crab, pos) for crab in crabs)

def crabs_naive(crabs, max_position, cost_counter):
    minimum = None
    for pos in range(max_position):
        cost = move_crabs(crabs, pos, cost_counter)
        if not minimum or cost < minimum:
            minimum = cost
    return minimum

def crabs_by_median(crabs):
    median = sorted(crabs)[len(crabs)//2]
    return sum(abs(median - crab) for crab in crabs)

raw_data = '''16,1,2,0,4,2,7,1,2,14'''

print('Tests...')
crabs = list(map(int, raw_data.split(',')))
print('Cheap crabs:', int(crabs_naive(crabs, max(crabs), lambda a, b: abs(b - a))) == 37)
print('Cheap crabs (non naive):', int(crabs_by_median(crabs)) == 37)
print('Expensive crabs:', (int(crabs_naive(crabs, max(crabs), sum_range)) == 168))
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    crabs = list(map(int, raw_data.split(',')))
    print('Cheap crabs:', int(crabs_naive(crabs, max(crabs), lambda a, b: abs(b - a))))
    print('Cheap crabs (non naive):', int(crabs_by_median(crabs)))
    print('Expensive crabs:', (int(crabs_naive(crabs, max(crabs), sum_range))))
