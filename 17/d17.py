import re

print('Day 17 of Advent of Code!')


def get_target(data):
    regex = r'target area: x=(-?[\d]+)..(-?[\d]+), y=(-?[\d]+)..(-?[\d]+)'
    coords = list(map(int, re.findall(regex, data)[0]))
    x1, x2 = coords[0], coords[1]
    y1, y2 = coords[2], coords[3]
    return x1, x2, y1, y2

def step(bullet, dx, dy):
    x, y = bullet
    x += dx
    y += dy
    if dx > 0: dx -= 1
    elif dx < 0: dx += 1
    dy -= 1
    return (x, y), dx, dy

def is_in_target(bullet, target):
    x1, x2, y1, y2 = target
    x, y = bullet
    return x1 <= x <= x2 and y1 <= y <= y2

def is_miss(bullet, target, dx):
    x1, x2, y1, _ = target
    x, y = bullet
    return x > x2 or y < y1 or (x < x1 and dx == 0)

def simulate(target):
    x1, x2, y1, y2 = target

    scope_x = abs(max(x1, x2)) * 2
    scope_y = abs(max(y1, y2)) * 2

    max_ys = []
    bullet = (0, 0)

    for ix in range(scope_x):
        for iy in range(-scope_y, scope_y):
            bullet = (0, 0)
            max_y = bullet[1]
            dx, dy = ix, iy
            while not is_miss(bullet, target, dx):
                bullet, dx, dy = step(bullet, dx, dy)
                if bullet[1] > max_y:
                    max_y = bullet[1]
                if is_in_target(bullet, target):
                    max_ys.append(max_y)
                    break
    return max_ys

raw_data = 'target area: x=20..30, y=-10..-5'

print('Tests...')
max_ys = simulate(get_target(raw_data))
print(f'Highest throw: {sorted(max_ys)[-1] == 45}. Possible throws: {len(max_ys) == 112}.')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    max_ys = simulate(get_target(raw_data))
    print(f'Highest throw: {sorted(max_ys)[-1]}. Possible throws: {len(max_ys)}.')
