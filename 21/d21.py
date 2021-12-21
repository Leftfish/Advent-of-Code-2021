print('Day 11 of Advent of Code!')

raw_data = ''''''

def dice(start=1, sides=100):
    value = start
    while True:
        yield value
        if value == sides:
            value = start
        else:
            value += 1

def move(position, move, fields=10):
    return ((position - 1) + move) % fields + 1

d = dice(1, 3)

p1 = 4
p2 = 8
p1_score = 0
p2_score = 0
rolls = 0
MAX_SCORE = 21

while True:
    p1_move = sum([next(d), next(d), next(d)])
    rolls += 3
    p1 = move(p1, p1_move)
    p1_score += p1
    if p1_score >= MAX_SCORE: break
    
    p2_move = sum([next(d), next(d), next(d)])
    rolls += 3
    p2 = move(p2, p2_move)
    p2_score += p2
    if p2_score >= MAX_SCORE: break

print("P1:", p1, "MOVED BY", p1_move, "SCORE", p1_score)
print("P2:", p2,  "MOVED BY", p2_move, "SCORE", p2_score)
print(rolls * min(p1_score, p2_score))



print('Tests...')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
