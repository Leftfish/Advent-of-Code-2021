from typing import Dict, List, Set, Tuple
import re


print('Day 8 of Advent of Code!')


def process_line(line: str) -> Tuple[List[str], List[str]]:
    processed = re.findall(r'(\w+)', line)
    raw_input = processed[:10]
    raw_output = processed[10:]
    return raw_input, raw_output


def get_all_digits(raw_digits: List[str]) -> List[Set[chr]]:
    digits = []
    for digit in raw_digits:
        sd = set(digit)
        if sd not in digits:
            digits.append(sd)
    return digits


def count_easy_digits(lines: str) -> int:
    return sum(1 for line in lines for digit in process_line(line)[1] if len(digit) in (2, 3, 4, 7))


def decode_digits(raw_digits: List[str]) -> Dict[frozenset, chr]:
    digits = {}
    all_digits = sorted(get_all_digits(raw_digits), key=lambda s: len(s))

    ONE = frozenset(all_digits[0])
    FOUR = frozenset(all_digits[2])
    SEVEN = frozenset(all_digits[1])
    EIGHT = frozenset(all_digits[-1])

    digits[ONE] = '1'
    digits[FOUR] = '4'
    digits[SEVEN] = '7'
    digits[EIGHT] = '8'

    for number in all_digits[3:9]:
        if len(number) == 5 and len(ONE & number) == 2:
            digits[frozenset(number)] = '3'
        elif len(number) == 5 and len(FOUR & number) == 3:
            digits[frozenset(number)] = '5'
        elif len(number) == 5:
            digits[frozenset(number)] = '2'
        elif len(number) == 6 and len(FOUR & number) == 4:
            digits[frozenset(number)] = '9'
        elif len(number) == 6 and len(SEVEN & number) == 2:
            digits[frozenset(number)] = '6'
        else:
            digits[frozenset(number)] = '0'

    return digits


def get_output_number(line: str) -> int:
    raw_input, raw_output = process_line(line)
    digits = decode_digits(raw_input + raw_output)
    processed_output = ''.join(digits[frozenset(digit)] for digit in raw_output)
    return int(processed_output)


def sum_outputs(lines: List[str]) -> int:
    return sum(get_output_number(line) for line in lines)


raw_data = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''.splitlines()

print('Tests...')
print('Counting easy digits:', count_easy_digits(raw_data) == 26)
print('Sum of outputs:', sum_outputs(raw_data) == 61229)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read().splitlines()
    print('Counting easy digits:', count_easy_digits(raw_data))
    print('Sum of outputs:', sum_outputs(raw_data))
