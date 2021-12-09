print('Day 9 of Advent of Code!')


def get_height_map(data):
    height_map = []
    for line in data.splitlines():
        height_map.append(list(map(int, list(line))))
    return height_map


def get_risk_level(height_map, i, j):
    for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i,j-1), (i, j+1)]:
        if adj_i < 0 or adj_i >= len(height_map) or adj_j < 0 or adj_j >= len(height_map[0]): 
            continue
        if height_map[i][j] >= height_map[adj_i][adj_j]: 
            return 0
    return 1 + height_map[i][j]


def calculate_risk_level(height_map):
    return sum(get_risk_level(height_map, i, j) for i in range(len(height_map)) for j in range(len(height_map[0])))


def calculate_basin_areas(basin_map, visited, i, j):
    # this is essentially the problem of finding islands in a 2D matrix, but we check their sizes instead of counting them
    # if no adjacent up/down/left/right or adjacent visited or adjacent not in basin (value 9): return 0 (add no area)
    # otherwise: add the current to visited and basin size = current (which is 1) plus DFS up/down/left/right

    if i < 0 or i >= len(basin_map) or j < 0 or j >= len(basin_map[0]) or (i, j) in visited or basin_map[i][j] == 9:
        return 0
    else:
        visited.add((i, j))
        return (1 + calculate_basin_areas(basin_map, visited, i+1, j) + calculate_basin_areas(basin_map, visited, i-1, j) + calculate_basin_areas(basin_map, visited, i, j+1) + calculate_basin_areas(basin_map, visited, i, j-1))


def find_basin_areas(basin_map):
    visited = set()
    return sorted([calculate_basin_areas(basin_map, visited, i, j) for i in range(len(basin_map)) for j in range(len(basin_map[0]))])


raw_data = '''2199943210
3987894921
9856789892
8767896789
9899965678'''


print('Tests...')
height_map = get_height_map(raw_data)
basin_areas = find_basin_areas(height_map)
print('Risk level:', calculate_risk_level(height_map))
print('Product of three biggest basin_areas:', basin_areas[-3] * basin_areas[-2] * basin_areas[-1])
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()  
    height_map = get_height_map(raw_data)
    basin_areas = find_basin_areas(height_map)
    print('Risk level:', calculate_risk_level(height_map))
    print('Product of three biggest basin_areas:', basin_areas[-3] * basin_areas[-2] * basin_areas[-1])
