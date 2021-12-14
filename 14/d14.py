import re
from collections import Counter, defaultdict

print('Day 14 of Advent of Code!')

def parse_data(data):
    initial, raw_insertions = data.split('\n\n')
    insertions = defaultdict(str)
    pairs = defaultdict(int)
    element_counter = Counter(initial)
    regex = r'(\w+) -> (\w+)'

    for insertion in raw_insertions.splitlines():
        parsed = re.findall(regex, insertion)[0]
        insertions[parsed[0]] = parsed[1]

    raw_pairs = [initial[i:i+2] for i in range(len(initial))]

    for pair in raw_pairs:
        if len(pair) == 2:
            pairs[pair] += 1

    return pairs, insertions, element_counter

def split_pair(pair, instructions):
    first = pair[0] + instructions[pair]
    second = first[1] + pair[1]
    return first, second

def insert(pairs, instructions, element_counter):
    new_pairs = defaultdict(int)

    for pair in pairs:
        if pairs[pair] > 0:
            first, second = split_pair(pair, instructions)
            new_pairs[first] += pairs[pair]
            new_pairs[second] += pairs[pair]
            element_counter[first[1]] += pairs[pair]

    return new_pairs


def solve(pairs, instructions, element_counter, steps):
    for _ in range(steps):
        pairs = insert(pairs, instructions, element_counter)

    element_qtys = sorted(element_counter.values())

    return element_qtys[-1] - element_qtys[0]

raw_data = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

print('Tests...')
poly, inserts, counter = parse_data(raw_data)
print('Most common - least common after 10 insertions:', solve(poly, inserts, counter, 10) == 1588)
counter = parse_data(raw_data)[2] #reset element counter
print('Most common - least common after 40 insertions:', solve(poly, inserts, counter, 40) == 2188189693529)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    poly, inserts, counter = parse_data(raw_data)
    print('Most common - least common after 10 insertions:', solve(poly, inserts, counter, 10))
    counter = parse_data(raw_data)[2] #reset element counter
    print('Most common - least common after 40 insertions:', solve(poly, inserts, counter, 40))
