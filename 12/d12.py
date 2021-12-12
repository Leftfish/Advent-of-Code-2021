from collections import defaultdict

print('Day 12 of Advent of Code!')

def make_graph(data):
    graph = defaultdict(list)
    for line in data.splitlines():
        parsed = line.split('-')
        graph[parsed[0]].append(parsed[1])
        graph[parsed[1]].append(parsed[0])
    return graph

def find_all_paths(graph, current, path_so_far, flag):
    # this is not my original answer
    # after solving part 2 with a horribly inefficient method I started looking for something better
    # and I found this gem: https://github.com/ephemient/aoc2021/blob/main/py/aoc2021/day12.py
    # I had no idea yield from was even a thing in Python so I rewrote my original part 1 to include this tool
    
    if current == 'end':
        yield path_so_far + [current]
        
    else:
        for neigh in graph[current]:
            if neigh == 'start':
                pass
            elif neigh.isupper() or neigh not in path_so_far:
                yield from find_all_paths(graph, neigh, path_so_far + [neigh], flag)
            elif neigh.islower() and flag:
                # if the function starts with flag set to True, it runs here to allow a single small cave
                # to be visited twice. this line sets the flag back to False so no other small cave gets
                # visited twice
                yield from find_all_paths(graph, neigh, path_so_far + [neigh], False)

raw_data = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''


print('Tests...')
G = make_graph(raw_data)
print("Part 1:", len(list(find_all_paths(G, "start", ["start"], False))) == 10)
print("Part 2:", len(list(find_all_paths(G, "start", ["start"], True))) == 36)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    G = make_graph(raw_data)
    print("Part 1:", len(list(find_all_paths(G, "start", ["start"], False))))
    print("Part 2:", len(list(find_all_paths(G, "start", ["start"], True))))
