from statistics import median
from typing import List, Tuple

print('Day 10 of Advent of Code!')

OPEN = '({[<'
CLOSE = ')}]>'
CLOSE_TO_OPEN = dict(zip(CLOSE, OPEN))
SYNTAX_POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
AUTOCOMPLETE_POINTS = {'(': 1, '[': 2, '{': 3, '<': 4}
MULTIPLIER = 5
INCOMPLETE = 0
VALID = -1


def check_line(line: str) -> Tuple[int, List[chr]]:
    stack = []
    for char in line:
        if char in OPEN:
            stack.append(char)
        else:
            if CLOSE_TO_OPEN[char] == stack[-1]:
                stack.pop()
            else:
                return ord(char), stack
    if stack:
        return INCOMPLETE, stack
    else:
        return VALID, stack


def sum_points(data: str) -> Tuple[int, int]:
    score_syntax = 0
    scores_autocomplete = []
    for line in data.splitlines():
        validation_data = check_line(line)
        if validation_data[0] == INCOMPLETE:
            stack = validation_data[1]
            line_score = 0
            while stack:
                current = stack.pop()
                line_score *= MULTIPLIER
                line_score += AUTOCOMPLETE_POINTS[current]
            scores_autocomplete.append(line_score)
        elif validation_data[0] != VALID:
            incorrent_char = chr(validation_data[0])
            score_syntax += SYNTAX_POINTS[incorrent_char]
    return score_syntax, median(sorted(scores_autocomplete))


raw_data = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''


print('Tests...')
scores = sum_points(raw_data)
print('Syntax checker score:', scores[0] == 26397)
print('Autocomplete score:', scores[1] == 288957)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    scores = sum_points(raw_data)
    print('Syntax checker score:', scores[0])
    print('Autocomplete score:', scores[1])
