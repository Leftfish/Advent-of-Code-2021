from collections import defaultdict
from queue import PriorityQueue

print('Day 15 of Advent of Code!')

MAX_RISK = 9

class Graph:
    def __init__(self, data):
        self.number_of_vertices = len(data[0]) * len(data)
        self.edges = defaultdict(list)
        for i in range(len(data)):
            for j in range(len(data[0])):    
                for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i,j-1), (i, j+1)]:
                    if adj_i < 0 or adj_i >= len(data) or adj_j < 0 or adj_j >= len(data[0]): 
                        continue
                    else:
                        neighbor_coords = (adj_i, adj_j)
                        neighbor_weight = data[adj_i][adj_j]
                        self.edges[(i, j)].append((neighbor_coords, neighbor_weight))

    def dijkstra(self, start):
        distances = {vertex:float('inf') for vertex in self.edges}
        distances[start] = 0
        visited = set()
        
        pq = PriorityQueue()
        pq.put((0, start))
        
        while not pq.empty():
            _, current_vertex = pq.get()
            visited.add(current_vertex)

            for neighbor in self.edges[current_vertex]:
                neighbor_coords, neighbor_dist = neighbor
                distance = neighbor_dist
                if neighbor[0] not in visited:
                    old_cost = distances[neighbor_coords]
                    new_cost = distances[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor_coords))
                        distances[neighbor_coords] = new_cost
        return distances
        
def new_risk(risk, delta):
        for _ in range(delta):
            risk += 1
            if risk > MAX_RISK:
                risk = 1
        return risk

def expand_right(cave_map, times):    
    tile_size = len(cave_map[0])
    for t in range(1, times):
        for line in cave_map:
            for i in range(tile_size):
                line.append(new_risk(line[i], t))
    return cave_map

def expand_down(cave_map, times):
    tile_size = len(cave_map)
    for t in range(1, times):
        for i in range(tile_size):
            new_line = [new_risk(value, t) for value in cave_map[i]]
            cave_map.append(new_line)
    return cave_map
    
raw_data = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

print('Tests...')
data = [list(map(int, list(line))) for line in raw_data.splitlines()]
small_cave = Graph(data)
start = (0,0)
end = (len(data)-1, len(data[0])-1)
print('Shortest path in the cavern:', small_cave.dijkstra(start)[end] == 40)
data = expand_right(data, 5)
data = expand_down(data, 5)
big_cave = Graph(data)
end = (len(data)-1, len(data[0])-1)
print('Shortest path in the entire cave:', big_cave.dijkstra(start)[end] == 315)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    data = [list(map(int, list(line))) for line in raw_data.splitlines()]
    small_cave = Graph(data)
    start = (0,0)
    end = (len(data)-1, len(data[0])-1)
    print('Shortest path in the cavern:', small_cave.dijkstra(start)[end])
    data = expand_right(data, 5)
    data = expand_down(data, 5)
    big_cave = Graph(data)
    end = (len(data)-1, len(data[0])-1)
    print('Shortest path in the entire cave:', big_cave.dijkstra(start)[end])
