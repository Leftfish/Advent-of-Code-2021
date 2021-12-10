from collections import deque

print('Day 9 of Advent of Code!')

def get_height_map(data):
    height_map = []
    for line in data.splitlines():
        height_map.append(list(map(int, list(line))))
    return height_map


def calculate_area_risk_level(height_map, i, j):
    for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i,j-1), (i, j+1)]:
        if adj_i < 0 or adj_i >= len(height_map) or adj_j < 0 or adj_j >= len(height_map[0]): 
            continue
        if height_map[i][j] >= height_map[adj_i][adj_j]: 
            return 0
    return 1 + height_map[i][j]


def calculate_total_risk_level(height_map):
    return sum(calculate_area_risk_level(height_map, i, j) for i in range(len(height_map)) for j in range(len(height_map[0])))


def calc_areas_dfs(height_map, visited, i, j):
    # this is essentially the problem of finding islands in a 2D matrix, but we check their sizes instead of counting them
    # if no adjacent up/down/left/right or adjacent visited or adjacent not in basin (value 9): return 0 (add no area)
    # otherwise: add the current to visited and basin size = current (which is 1) plus DFS up/down/left/right

    if i < 0 or i >= len(height_map) or j < 0 or j >= len(height_map[0]) or (i, j) in visited or height_map[i][j] == 9:
        return 0
    else:
        visited.add((i, j))
        return (1 + calc_areas_dfs(height_map, visited, i+1, j) + calc_areas_dfs(height_map, visited, i-1, j) + calc_areas_dfs(height_map, visited, i, j+1) + calc_areas_dfs(height_map, visited, i, j-1))


def find_all_areas_dfs(height_map):
    visited = set()
    return sorted([calc_areas_dfs(height_map, visited, i, j) for i in range(len(height_map)) for j in range(len(height_map[0]))])


def find_all_areas_bfs(height_map):
    # iterate through 2d matrix
    # if the current area is not visited and is in basin (value not 9): perform BFS
    # iterative BFS: start a queue, add current to queue if not already visited, increment area
    # and iterate through adjacent - if they exist (i.e. not out of bounds) and are in basin (value not 9)
    # then add them to queue. repeat until queue not empty.
    
    all_areas = []
    visited = set()

    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            if (i, j) not in visited and height_map[i][j] != 9:
                current_area = 0
                Q = deque()
                Q.append((i, j))

                while Q:
                    (i, j) = Q.popleft()
                    if (i, j) in visited:
                        continue
                    visited.add((i, j))

                    current_area += 1

                    for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i,j-1), (i, j+1)]:
                            if adj_i < 0 or adj_i >= len(height_map) or adj_j < 0 or adj_j >= len(height_map[0]): 
                                continue
                            else:
                                if height_map[adj_i][adj_j] != 9:
                                    Q.append((adj_i, adj_j))

                all_areas.append(current_area)

    return sorted(all_areas)


raw_data = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

print('Tests...')
height_map = get_height_map(raw_data)
basin_areas = find_all_areas_dfs(height_map)
print('Risk level:', calculate_total_risk_level(height_map) == 15)
print('Product of three biggest basin areas (DFS):', basin_areas[-3] * basin_areas[-2] * basin_areas[-1] == 1134)
basin_areas = find_all_areas_bfs(height_map)
print('Product of three biggest basin areas (BFS):', basin_areas[-3] * basin_areas[-2] * basin_areas[-1] == 1134)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()  
    height_map = get_height_map(raw_data)
    basin_areas = find_all_areas_dfs(height_map)
    print('Risk level:', calculate_total_risk_level(height_map))
    print('Product of three biggest basin areas (DFS):', basin_areas[-3] * basin_areas[-2] * basin_areas[-1])
    basin_areas = find_all_areas_bfs(height_map)
    print('Product of three biggest basin areas (BFS):', basin_areas[-3] * basin_areas[-2] * basin_areas[-1])
