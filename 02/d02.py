print('Day 2 of Advent of Code!')

def calculate_position(data):
    position = complex(0, 0)
    moves = data.splitlines()
    for move in moves:
        direction, distance = move.split()
        distance = int(distance)
        if direction[0] == 'f':
            position += complex(distance, 0)
        elif direction[0] == 'd':
            position += complex(0, distance)
        elif direction[0] == 'u':
            position += complex(0, -distance)
    return position

def calculate_position_aim(data):
    position = complex(0, 0)
    aim = 0
    moves = data.splitlines()
    for move in moves:
        direction, distance = move.split()
        distance = int(distance)
        if direction[0] == 'f':
            position += complex(distance, 0)
            position += complex(0, aim * distance)
        elif direction[0] == 'd':
            aim += distance
        elif direction[0] == 'u':
            aim -= distance
    return position

test_data = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''

print('Tests...')
positions = calculate_position(test_data), calculate_position_aim(test_data)
print('Position before using the manual:',  int(positions[0].real * positions[0].imag) == 150)
print('Position after using the manual:',  int(positions[1].real * positions[1].imag) == 900)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    data = inp.read()
    positions = calculate_position(data), calculate_position_aim(data)
    print('Position before using the manual:',  int(positions[0].real * positions[0].imag))
    print('Position after using the manual:',  int(positions[1].real * positions[1].imag))
