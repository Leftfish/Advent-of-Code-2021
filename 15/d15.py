import heapq
from collections import defaultdict

print('Day 15 of Advent of Code!')

MAX_RISK = 9


class Graph:
    def __init__(self, data):
        self.number_of_vertices = len(data[0]) * len(data)
        self.edges = defaultdict(list)
        for i in range(len(data)):
            for j in range(len(data[0])):
                for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                        neighbor_coords = (adj_i, adj_j)
                        neighbor_weight = data[adj_i][adj_j]
                        self.edges[(i, j)].append((neighbor_coords, neighbor_weight))

    def dijkstra(self, start):
        distances = {vertex: float('inf') for vertex in self.edges}
        distances[start] = 0
        visited = set()

        pq = []
        heapq.heapify(pq)
        heapq.heappush(pq, (0, start))

        while pq:
            _, current_vertex = heapq.heappop(pq)
            visited.add(current_vertex)

            for neighbor in self.edges[current_vertex]:
                neighbor_coords, neighbor_dist = neighbor
                distance = neighbor_dist
                if neighbor[0] not in visited:
                    old_cost = distances[neighbor_coords]
                    new_cost = distances[current_vertex] + distance
                    if new_cost < old_cost:
                        heapq.heappush(pq, (new_cost, neighbor_coords))
                        distances[neighbor_coords] = new_cost
        return distances


def new_risk(risk, delta):
        return (risk + delta - 1) % MAX_RISK + 1


def expand_cave(cave_map, times):
    height, width = len(cave_map), len(cave_map[0])
    for delta in range(1, times): # expand right
        for line in cave_map:
            for i in range(width):
                line.append(new_risk(line[i], delta))
    for delta in range(1, times): # expand down
        for i in range(height):
            new_line = [new_risk(value, delta) for value in cave_map[i]]
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
start = (0, 0)
end = (len(data)-1, len(data[0])-1)
print('Shortest path in the cavern:', small_cave.dijkstra(start)[end] == 40)
big_cave = Graph(expand_cave(data, 5))
end = (len(data)-1, len(data[0])-1)
print('Shortest path in the entire cave:', big_cave.dijkstra(start)[end] == 315)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    data = [list(map(int, list(line))) for line in raw_data.splitlines()]
    small_cave = Graph(data)
    start = (0, 0)
    end = (len(data)-1, len(data[0])-1)
    print('Shortest path in the cavern:', small_cave.dijkstra(start)[end])
    big_cave = Graph(expand_cave(data, 5))
    end = (len(data)-1, len(data[0])-1)
    print('Shortest path in the entire cave:', big_cave.dijkstra(start)[end])
