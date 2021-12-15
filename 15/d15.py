from collections import defaultdict
from queue import PriorityQueue

print('Day 15 of Advent of Code!')

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
            (dist, current_vertex) = pq.get()
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

data = [list(map(int, list(line))) for line in raw_data.splitlines()]
G = Graph(data)
start = (0,0)
end = (len(data)-1, len(data[0])-1)
print(G.dijkstra(start)[end])


print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    data = [list(map(int, list(line))) for line in raw_data.splitlines()]
    G = Graph(data)
    start = (0,0)
    end = (len(data)-1, len(data[0])-1)
    print(G.dijkstra(start)[end])