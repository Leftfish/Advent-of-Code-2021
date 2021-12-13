import numpy as np
import re

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
points, instructions = parse_data(raw_data)
paper = make_paper(points)
solve(paper, instructions)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    points, instructions = parse_data(raw_data)
    paper = make_paper(points)
    solve(paper, instructions)