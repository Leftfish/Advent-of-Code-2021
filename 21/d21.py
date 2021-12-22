import re
from itertools import cycle, product
from functools import lru_cache

print('Day 21 of Advent of Code!')

def move(position, move, fields=10):
    return ((position - 1) + move) % fields + 1

def warmup_game(p1, p2, max_score):
    d = cycle(range(1,101))
    p1_score = 0
    p2_score = 0
    rolls = 0
    rolls_per_turn = 3

    while True:
        p1_move = sum([next(d) for _ in range(rolls_per_turn)])
        rolls += rolls_per_turn
        p1 = move(p1, p1_move)
        p1_score += p1
        if p1_score >= max_score: break
        
        p2_move = sum([next(d) for _ in range(rolls_per_turn)])
        rolls += rolls_per_turn
        p2 = move(p2, p2_move)
        p2_score += p2
        if p2_score >= max_score: break

    return rolls * min(p1_score, p2_score)

dirac_dice_throws = list(product([1,2,3], repeat=3))

@lru_cache(maxsize=None)
def doctor_strange(p1, p2, p1_score, p2_score, win):

    wins = {'P1': 0, 'P2': 0}

    for p1_throw in dirac_dice_throws:
        for p2_throw in dirac_dice_throws:
            p1_new_pos = move(p1, sum(p1_throw))
            p2_new_pos = move(p2, sum(p2_throw))
            p1_new_score = p1_score + p1_new_pos
            p2_new_score = p2_score + p2_new_pos

            if p1_new_score >= win:
                wins['P1'] += 1
                break
            if p2_new_score >= win:
                wins['P2'] += 1
                continue
            new_universe = doctor_strange(p1_new_pos, p2_new_pos, p1_new_score, p2_new_score, win)
            wins['P1'] += new_universe['P1']
            wins['P2'] += new_universe['P2']
    return wins

print('Tests...')
print('Warmup game (throws * losing score):', warmup_game(4, 8, 1000) == 739785)
print('Multiverse game (max wins):', max(doctor_strange(4, 8, 0, 0, 21).values()) == 444356092776315)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    players = [int(re.findall(r'starting position: (\d+)', line)[0]) for line in inp.readlines()]
    print('Warmup game (throws * losing score):', warmup_game(players[0], players[1], 1000))
    print('Multiverse game (max wins):', max(doctor_strange(players[0], players[1], 0, 0, 21).values()))
