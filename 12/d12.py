from collections import defaultdict, deque
from collections import Counter

print('Day 12 of Advent of Code!')

raw_data = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

raw_data = '''by-TW
start-TW
fw-end
QZ-end
JH-by
ka-start
ka-by
end-JH
QZ-cv
vg-TI
by-fw
QZ-by
JH-ka
JH-vg
vg-fw
TW-cv
QZ-vg
ka-TW
ka-QZ
JH-fw
vg-hu
cv-start
by-cv
ka-cv'''

def make_graph(data):
    graph = defaultdict(list)
    for line in data.splitlines():
        parsed = line.split('-')
        graph[parsed[0]].append(parsed[1])
        graph[parsed[1]].append(parsed[0])
    return graph

PATHS = set()
PATHS_TWO = set()

def verify_path(path):
    C = Counter(path)
    small_visited_twice = 0
    for v in C:
        if v.islower() and C[v] > 1:
            small_visited_twice += 1
            if small_visited_twice > 1:
                return False
    return True

def find_paths_small_once(graph, path_so_far):
    current = path_so_far[-1]
    #print(f'1: current {current}, pathsofar {path_so_far}, neighs {graph[current]}')
    for neigh in graph[current]:
        #print(f'2: current {current}, neigh {neigh} in g[c] {graph[current]}')
        #if neigh=='end': print('---->', path_so_far + [neigh])
        if neigh == 'end' or (neigh.islower() and neigh in path_so_far):
            if neigh=='end': 
                PATHS.add(" -> ".join(path_so_far + [neigh]))
        else:
            #print(f'3. current {current}, neigh {neigh} not in path so far {path_so_far}, recursing with {path_so_far + [neigh]}')
            find_paths_small_once(graph, path_so_far + [neigh])

def find_paths_small_twice(graph, path_so_far):
    current = path_so_far[-1]
    #print(f'1: current {current}, pathsofar {path_so_far}, neighs {graph[current]}')
    for neigh in graph[current]:
        #print(f'2: current {current}, neigh {neigh} in g[c] {graph[current]}')
        #if neigh=='end': print('---->', path_so_far + [neigh])
        if neigh == 'end' or neigh == 'start' or (neigh.islower() and path_so_far.count(neigh) > 1):
            if neigh=='end' and verify_path(path_so_far + [neigh]): 
                PATHS_TWO.add(" -> ".join(path_so_far + [neigh]))
                if not len(PATHS_TWO)%1000: print(len(PATHS_TWO))
        else:
            #print(f'3. current {current}, neigh {neigh} not in path so far {path_so_far}, recursing with {path_so_far + [neigh]}')
            find_paths_small_twice(graph, path_so_far + [neigh])

G = make_graph(raw_data)

find_paths_small_twice(G, ['start'])
#for p in PATHS_TWO:
#    print(p)
print(len(PATHS_TWO))




path = 'start -> A -> c -> A -> b -> A -> b -> A -> c -> A -> end'
p = path.split(' -> ')
print(path)
print(verify_path(p))
path = 'start -> A -> b -> A -> b -> A -> c -> A -> end'
print(path)
p = path.split(' -> ')
print(verify_path(p))


print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
