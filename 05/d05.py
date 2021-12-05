from collections import defaultdict
from typing import DefaultDict
import matplotlib.pyplot as plt
import random
import re

print('Day 5 of Advent of Code!')

SHADES_OF_GRAY = ['#' + 3 * hex(i)[2:] for i in range(40, 200, 10)]
PLOT_SIZE = 800
DPI = 96


def get_lines(data: str) -> set:
    lines = set()
    for line in data.splitlines():
        coordinates = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line).groups()
        start = tuple(map(int,[coordinates[0], coordinates[1]]))
        stop = tuple(map(int,[coordinates[2], coordinates[3]]))
        lines.add((start, stop))
    return lines


def find_occupied_points(lines: list, count_diagonal=False) -> DefaultDict:
    occupied_points = defaultdict(int)

    for line in lines:
        start_x, stop_x = line[0][0], line[1][0]
        start_y, stop_y = line[0][1], line[1][1]
        x, y = start_x, start_y
        dx = -1 if start_x > stop_x else 1
        dy = -1 if start_y > stop_y else 1

        if start_x == stop_x:
            occupied_points[(x, y)] += 1
            while y != stop_y:
                y += dy
                occupied_points[(x, y)] += 1
        
        elif start_y == stop_y:            
            occupied_points[(x, y)] += 1
            while x != stop_x:
                x += dx
                occupied_points[(x, y)] += 1

        elif count_diagonal:
            occupied_points[(x, y)] += 1
            while x != stop_x:
                x += dx
                y += dy
                occupied_points[(x, y)] += 1
    
    return occupied_points


def count_intersections(occupied_points: DefaultDict) -> int:
    return sum(1 for intersections in occupied_points.values() if intersections > 1)


def draw_lines(lines: set) -> None:
    plt.figure(num='Hydrothermal vents', figsize=(PLOT_SIZE/DPI, PLOT_SIZE/DPI), dpi=DPI)

    ax=plt.axes()
    ax.set_facecolor('#000000')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    for line in lines:
        xs = (line[0][0], line[1][0])
        ys = (line[0][1], line[1][1])
        plt.plot(xs, ys,color=random.choice(SHADES_OF_GRAY), linewidth=1)

    plt.show()


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
print('Only horizontal and vertical:', count_intersections(find_occupied_points(lines)) == 5)
print('Horizontal, vertical and diagonal:', count_intersections(find_occupied_points(lines, True)) == 12)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    lines = get_lines(inp.read())
    print('Only horizontal and vertical:', count_intersections(find_occupied_points(lines)))
    print('Horizontal, vertical and diagonal:', count_intersections(find_occupied_points(lines, True)))
    draw_lines(lines)
