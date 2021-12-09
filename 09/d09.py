print('Day 9 of Advent of Code!')


def get_height_map(data: str) -> list:
    height_map = []
    for line in data.splitlines():
        height_map.append(list(map(int, list(line))))
    return height_map


def get_risk_level(height_map, i, j) -> int:
    current = height_map[i][j]
    for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i,j-1), (i, j+1)]:
        if adj_i < 0 or adj_i >= len(height_map) or adj_j < 0 or adj_j >= len(height_map[0]): 
            continue
        if current >= height_map[adj_i][adj_j]: 
            return 0
    return 1 + current


def calculate_risk_level(height_map):
    total_risk_level = 0
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            current_risk_level =  get_risk_level(height_map, i, j)
            total_risk_level += current_risk_level
    return total_risk_level


def dfs_area(basin_map, visited, i, j):
    # if no adjacent up/down/left/right or adjacent visited or adjacent not in basin (value 9): return 0 (add no area)
    if i < 0 or i >= len(basin_map) or j < 0 or j >= len(basin_map[0]) or (i, j) in visited or basin_map[i][j] == 9:
        return 0
    else:
    # otherwise: add the current to visited and basin size = current (which is 1) plus dfs up/down/left/right
        visited.add((i, j))
        return (1 + dfs_area(basin_map, visited, i+1, j) + dfs_area(basin_map, visited, i-1, j) + dfs_area(basin_map, visited, i, j+1) + dfs_area(basin_map, visited, i, j-1))


def find_basin_areas(basin_map):
    seen = set()
    return sorted([dfs_area(basin_map, seen, i, j) for i in range(len(basin_map)) for j in range(len(basin_map[0]))])




raw_data = '''2199943210
3987894921
9856789892
8767896789
9899965678'''


print('Tests...')
height_map = get_height_map(raw_data)
basins = find_basin_areas(height_map)
print('Risk level:', calculate_risk_level(height_map))
print('Product of three biggest basins:', basins[-3] * basins[-2] * basins[-1])

print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()  
    height_map = get_height_map(raw_data)
    basins = find_basin_areas(height_map)
    print('Risk level:', calculate_risk_level(height_map))
    print('Product of three biggest basins:', basins[-3] * basins[-2] * basins[-1])
