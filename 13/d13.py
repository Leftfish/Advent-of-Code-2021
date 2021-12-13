import numpy as np
import re
from copy import copy


print('Day 13 of Advent of Code!')


def parse_data(data):
    raw_points, raw_instructions = data.split('\n\n')
    regex = r'fold along (\w+)=(\d+)'
    points = set()
    instructions = list()

    for rp in raw_points.splitlines():
        coords = tuple(map(int, rp.split(',')))
        points.add(coords)

    for ri in raw_instructions.splitlines():
        instruction = re.findall(regex, ri)[0]
        instructions.append((instruction[0], int(instruction[1])))
    
    return points, instructions

def make_paper(points):
    height = max(pt[0] for pt in points) + 1
    width = max(pt[1] for pt in points) + 1
    paper = np.zeros((width, height))
    for point in points:
        y, x = point[0], point[1]
        paper[x][y] = 1
    return paper

def fold(paper, instruction):
    direction, line = instruction
    if direction == 'y':
        for x in range(len(paper[0])):
            for y in range(-1, -line-1, -1):
                if paper[y][x]:
                    ny = -(y + 1)
                    paper[y][x] = 0
                    paper[ny][x] = 1
        paper = paper[:line, :]
    if direction == 'x':
        for y in range(len(paper)):
            for x in range(-1, -line-1, -1):
                if paper[y][x]:
                    nx = -(x + 1)
                    paper[y][x] = 0
                    paper[y][nx] = 1
        paper = paper[:, :line]
    return paper

def print_paper(paper):
    for line in paper:
        line = ['#' if char == 1 else ' 'for char in line]
        print(''.join(line))

def solve(paper, instructions):
        for i, instruction in enumerate(instructions):
            paper = fold(paper, instruction)
            if i == 0:
                print(f'Points after first fold: {sum(sum(int(c) for c in line) for line in paper)}')
        print('Paper after folding:')
        print_paper(paper)


def points_to_dict(points):
    dict_points = dict()
    for point in points:
        dict_points[point] = 1
    return dict_points

def fold_without_drawing(points, axis, line):
    new_points = copy(points)
    for point in points:
        x, y = point[0], point[1]
        new_point = None
        if axis == 'x' and x > line:    
            new_point = (x - 2 * (x - line), y)
        elif axis == 'y' and y > line:
            new_point = (x, y - 2 * (y - line))
        if new_point:
            new_points[new_point] = 1
            new_points.pop(point, None)
    return new_points

def print_from_points(points):
    height = max(pt[0] for pt in points) + 1
    width = max(pt[1] for pt in points) + 1
    paper = np.zeros((width, height))
    for point in points.keys():
        y, x = point[0], point[1]
        paper[x][y] = 1
    for line in paper:
        line = ['#' if char == 1 else ' 'for char in line]
        print(''.join(line))

def solve_without_drawing(points, instructions):
    for i, instruction in enumerate(instructions):
        axis, line = instruction[0], instruction[1]
        points = fold_without_drawing(points, axis, line)
        if i == 0:
                print(f'Points after first fold: {len(points)}')
    print('Paper after folding:')
    print_from_points(points)

raw_data = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

print('Tests...')
print('Solving the hard way - with a 2D array...')
points, instructions = parse_data(raw_data)
solve(make_paper(points), instructions)
print('Solving the easy way - with a dictionary of points...')
solve_without_drawing(points_to_dict(points), instructions)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print('Solving the hard way - with a 2D array...')
    points, instructions = parse_data(raw_data)
    solve(make_paper(points), instructions)
    print('Solving the easy way - with a dictionary of points...')
    solve_without_drawing(points_to_dict(points), instructions)