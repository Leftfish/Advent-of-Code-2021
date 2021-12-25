print('Day 25 of Advent of Code!')

RGT = '>'
DWN = 'v'
CCMB = {RGT, DWN}

def parse_data(raw_data):
    bottom = {}
    max_i = len(raw_data) - 1
    max_j = len(raw_data[0]) - 1

    for i in range(len(raw_data)):
        for j in range(len(raw_data[0])):
            if raw_data[i][j] == RGT:
                bottom[(i,j)] = RGT
            elif raw_data[i][j] == DWN:
                bottom[(i,j)] = DWN

    return bottom, max_i, max_j

def get_nxt_right(j, max_j):
    return 0 if j == max_j else j + 1

def get_nxt_down(i, max_i):
    return 0 if i == max_i else i + 1

def play_turn(bottom, max_i, max_j):
    to_move_right = set()
    to_move_down = set()
    for field in bottom:
        if bottom[field] == RGT:
            nxt_right = get_nxt_right(field[1], max_j)
            if not bottom.get((field[0], nxt_right), None):
                to_move_right.add((field, nxt_right))
    for mover, new_j in to_move_right:
        i, j = mover
        del bottom[(i, j)]
        bottom[(i, new_j)] = RGT
    
    for field in bottom:
        if bottom[field] == DWN:
            nxt_down = get_nxt_down(field[0], max_i)
            if not bottom.get((nxt_down, field[1]), None):
                to_move_down.add((field, nxt_down))
    
    for mover, new_i in to_move_down:
        i, j = mover
        del bottom[(i, j)]
        bottom[(new_i, j)] = DWN

    number_moved = len(to_move_down) + len(to_move_right)

    return bottom, number_moved

def move_cucumbers(bottom, max_i, max_j):
    i = 0
    while True:
        bottom, number_moved = play_turn(bottom, max_i, max_j)
        i += 1
        if number_moved == 0:
            return i


raw_data = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''.splitlines()

print('Tests...')
print(f'Cucumbers stopped moving after {move_cucumbers(*parse_data(raw_data))} turns.')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read().splitlines()
    print(f'Cucumbers stopped moving after {move_cucumbers(*parse_data(raw_data))} turns.')
    
