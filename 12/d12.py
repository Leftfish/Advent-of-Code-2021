from collections import defaultdict, deque

print('Day 12 of Advent of Code!')

raw_data = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''


def make_graph(data):
    graph = defaultdict(list)
    for line in data.splitlines():
        parsed = line.split('-')
        graph[parsed[0]].append(parsed[1])
        graph[parsed[1]].append(parsed[0])
    return graph

PATHS = set()

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

G = make_graph(raw_data)

find_paths_small_once(G, ['start'])
for p in PATHS:
    print(p)
print(len(PATHS))



#print(G)


#print(dfs(G, path=['start'], paths=[]))

print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()

'''def find_all_paths(graph, start, end, being_visited, current_path):
    being_visited.add(start)
    if start == end:
        print(current_path)
        return
    for adj in graph[start]:
        if adj not in being_visited:
            current_path.append(adj)
            find_all_paths(graph, adj, end, being_visited, current_path)
            current_path.pop()

    being_visited.remove(start)


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths 
'''