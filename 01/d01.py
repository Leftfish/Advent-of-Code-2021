print('Day 1 of Advent of Code!')


def count_depth_increase(measurements):
    return sum(1 for i in range(1, len(measurements)) if measurements[i] > measurements[i-1])


test_data = '''199
200
208
210
200
207
240
269
260
263'''

test_measurements = [int(line.rstrip()) for line in test_data.splitlines()]
test_measurements_adjusted = [sum(test_measurements[i:i+3]) for i in range(len(test_measurements))]

print('Tests...')
print("Checking number of depth increases in test data: ", count_depth_increase(test_measurements) == 7)
print("Checking number of depth increases in test data, secondd method: ", count_depth_increase(test_measurements_adjusted) == 5)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    measurements = [int(line.rstrip()) for line in inp]
    measurements_adjusted = [sum(measurements[i:i+3]) for i in range(len(measurements))]
    print("Checking number of depth increases in input data: ", count_depth_increase(measurements))
    print("Checking number of depth increases in input data, second method: ", count_depth_increase(measurements_adjusted))
    