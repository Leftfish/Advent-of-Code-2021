import re


print('Day 8 of Advent of Code!')


def process_line(line):
    processed = re.findall(r'(\w+)', line)
    raw_input = processed[:10]
    raw_output = processed[10:]
    return raw_input, raw_output


def get_all_digits(line):
    inp, out = process_line(line)
    digits = []
    for digit in inp+out:
        sd = set(digit)
        if sd not in digits:
            digits.append(sd)
    return digits


def count_easy_digits(lines):
    return sum(1 for line in lines for digit in process_line(line)[1] if len(digit) in (2, 3, 4, 7))


def decode_digits(line):
    digits = {}
    all_digits = sorted(get_all_digits(line),  key = lambda s: len(s))
    
    ONE = frozenset(all_digits[0])
    FOUR = frozenset(all_digits[2])
    SEVEN = frozenset(all_digits[1])
    EIGHT = frozenset(all_digits[-1])
    
    digits[ONE] = '1'
    digits[SEVEN] = '7'
    digits[FOUR] = '4'
    digits[EIGHT] = '8'

    five_digits, six_digits = all_digits[3:6], all_digits[6:9]

    for number in six_digits:
        if FOUR <= number:
            digits[frozenset(number)] = '9'
            six_digits.remove(number)
    
    for number in six_digits:
        if ONE <= number:
            ZERO = frozenset(number)
            digits[ZERO] = '0'
            six_digits.remove(number)
            SIX = frozenset(six_digits.pop())
            digits[SIX] = '6'
    
    for number in five_digits:
        if ONE <= number:
            THREE = frozenset(number)
            digits[THREE] = '3'
            five_digits.remove(number)
    
    for number in five_digits:
        if number <= SIX:
            FIVE = frozenset(number)
            digits[FIVE] = '5'
            five_digits.remove(number)
            TWO = frozenset(five_digits.pop())
            digits[TWO] = '2'

    return digits


def get_output_number(line):
    digits = decode_digits(line)
    _, raw_output = process_line(line)
    processed_output = ''.join(digits[frozenset(digit)] for digit in raw_output)

    return int(processed_output)


def sum_outputs(lines):
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