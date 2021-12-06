from collections import Counter, deque

print('Day 6 of Advent of Code!')


def get_fish(data: str) -> deque:
    fish_counter = Counter(map(int, data.split(',')))
    fish_population = deque([0 for _ in range(9)])
    for fish in fish_counter:
        fish_population[fish] = fish_counter[fish]
    return fish_population


def simulate_day(fish_population: deque) -> deque:
    to_breed = fish_population[0]
    fish_population.rotate(-1)
    fish_population[6] += to_breed
    fish_population[8] = to_breed
    return fish_population


def simulate(fish_population: deque, days: int) -> int:
    for i in range(days):
        fish_population = simulate_day(fish_population)
    return sum(fish_population)


test_data = '''3,4,3,1,2'''

print('Tests...')
print('After 80 days:', simulate(get_fish(test_data), 80) == 5934)
print('After 256 days:', simulate(get_fish(test_data), 256) == 26984457539)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print('After 80 days:', simulate(get_fish(raw_data), 80))
    print('After 256 days:', simulate(get_fish(raw_data), 256))
