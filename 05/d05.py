from collections import defaultdict
from typing import DefaultDict
import re

print('Day 5 of Advent of Code!')


def get_lines(data: str) -> set:
    lines = set()
    for line in data.splitlines():
        coordinates = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line).groups()
        start = tuple(map(int,[coordinates[0], coordinates[1]]))
        stop = tuple(map(int,[coordinates[2], coordinates[3]]))
        lines.add((start, stop))
    return lines


def draw_lines(lines: list, count_diagonal=False) -> DefaultDict:
    occupied_points = defaultdict(int)

    for line in lines:
        start_x, stop_x = line[0][0], line[1][0]
        start_y, stop_y = line[0][1], line[1][1]
        current_x, current_y = start_x, start_y
        dx = -1 if start_x > stop_x else 1
        dy = -1 if start_y > stop_y else 1

        if start_x == stop_x:
            occupied_points[(current_x, current_y)] += 1
            while current_y != stop_y:
                current_y += dy
                occupied_points[(start_x, current_y)] += 1
        
        elif start_y == stop_y:            
            occupied_points[(current_x, current_y)] += 1
            while current_x != stop_x:
                current_x += dx
                occupied_points[(current_x, start_y)] += 1

        elif count_diagonal:
            occupied_points[(current_x, current_y)] += 1
            while current_x != stop_x:
                current_x += dx
                current_y += dy
                occupied_points[(current_x, current_y)] += 1
    
    return occupied_points


def count_intersections(occupied_points: DefaultDict) -> int:
    return sum(1 for intersections in occupied_points.values() if intersections > 1)


test_data = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''

print('Tests...')
lines = get_lines(test_data)
print('Only horizontal and vertical:', count_intersections(draw_lines(lines)) == 5)
print('Horizontal, vertical and diagonal:', count_intersections(draw_lines(lines, True)) == 12)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    lines = get_lines(inp.read())
    print('Only horizontal and vertical:', count_intersections(draw_lines(lines)))
    print('Horizontal, vertical and diagonal:', count_intersections(draw_lines(lines, True)))