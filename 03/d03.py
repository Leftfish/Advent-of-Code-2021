print('Day 3 of Advent of Code!')

from collections import defaultdict
from operator import ge, lt
from typing import Callable, Dict, List, Set


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


def filter_life_support_candidates(candidates: Set[str], bit_frequency: Dict[int, int], pos: int, comparator: Callable[[int, int], bool]) -> set:
    filtered_candidates = set()
    flag = '1' if comparator(bit_frequency[pos], len(candidates)/2) else '0'    

    for number in candidates:
        if number[pos] == flag:
            filtered_candidates.add(number)

    return filtered_candidates


def calculate_life_support(bits: List[str], bit_size: int) -> int:
    oxygen, co2 = ge, lt

    positions_oxy = count_ones(bits, bit_size)
    positions_co2 = count_ones(bits, bit_size)
    candidates_oxy = set(bits)
    candidates_co2 = set(bits)

    for bit_position in range(bit_size):
        if len(candidates_oxy) > 1:
            candidates_oxy = filter_life_support_candidates(candidates_oxy, positions_oxy, bit_position, oxygen)
            positions_oxy = count_ones(candidates_oxy, bit_size)

        if len(candidates_co2) > 1:
            candidates_co2 = filter_life_support_candidates(candidates_co2, positions_co2, bit_position, co2)
            positions_co2 = count_ones(candidates_co2, bit_size)

    oxy = candidates_oxy.pop()
    co2 = candidates_co2.pop()

    return int(oxy, 2) * int(co2, 2)


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
print('Life support rating:', calculate_life_support(bits, bit_size) == 230)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    bits = inp.read().splitlines()
    bit_size = len(bits[0])
    print('Power consumption:', calculate_power(bits, bit_size))
    print('Life support rating:', calculate_life_support(bits, bit_size))
