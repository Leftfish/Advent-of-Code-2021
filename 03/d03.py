print('Day 3 of Advent of Code!')

from collections import defaultdict
from operator import ge, lt
from typing import Callable, DefaultDict, List, Set


def count_ones(bits: List[str], bit_size: int) -> defaultdict:
    positions = defaultdict(int)
    for number in bits:
        for pos in range(bit_size):
            if number[pos] == '1':
                positions[pos] += 1
    return positions


def calculate_power(bits: List[str], bit_size: int) -> int:
    gamma = ''
    bit_frequency = count_ones(bits, bit_size)

    for i in range(bit_size):
        if bit_frequency[i] > len(bits)/2:
            gamma += '1'
        else:
            gamma += '0'

    epsilon = ''.join('1' if digit == '0' else '0' for digit in gamma)

    return int(gamma, 2) * int(epsilon, 2)


def filter_life_support_candidates(candidates: Set[str], bit_frequency: DefaultDict[int, int], pos: int, comparator: Callable[[int, int], bool]) -> Set[str]:
    flag = '1' if comparator(bit_frequency[pos], len(candidates)/2) else '0'        
    return set(number for number in candidates if number[pos] == flag)
    #return set(filter(lambda number: number[pos] == flag, candidates))


def get_life_support_rating(bits: List[str], bit_size: int, system: Callable[[int, int], bool]) -> int:
    positions = count_ones(bits, bit_size)
    candidates = set(bits)

    for bit_position in range(bit_size):
        if len(candidates) > 1:
            candidates = filter_life_support_candidates(candidates, positions, bit_position, system)
            positions = count_ones(candidates, bit_size)
        else:
            break

    return int(candidates.pop(), 2)


def calculate_life_support(bits: List[str], bit_size: int, oxygen: Callable[[int, int], bool], co2: Callable[[int, int], bool]) -> int:
    return get_life_support_rating(bits, bit_size, oxygen) * get_life_support_rating(bits, bit_size, co2)

test_data = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''

print('Tests...')
bits = test_data.splitlines()
bit_size = len(bits[0])
print('Power consumption:', calculate_power(bits, bit_size) == 198)
print('Life support rating:', calculate_life_support(bits, bit_size, ge, lt) == 230)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    bits = inp.read().splitlines()
    bit_size = len(bits[0])
    print('Power consumption:', calculate_power(bits, bit_size))
    print('Life support rating:', calculate_life_support(bits, bit_size, ge, lt))
