from collections import defaultdict

print('Day 20 of Advent of Code!')

NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
PADDING = 2

def get_picture(raw_pic: str) -> defaultdict:
    picture = defaultdict(int)
    for i in range(len(raw_pic)):
        for j in range(len(raw_pic[0])):
            picture[(i,j)] = 1 if raw_pic[i][j] == '#' else 0
    return picture

def decode_pixel(position: int, codec: str):
    return 1 if codec[position] == '#' else 0

with open('inp', mode='r') as inp:
    raw_data = inp.read().split('\n\n')
    codec = ''.join(raw_data[0].splitlines())
    pic = get_picture(raw_data[1].splitlines())
    
    steps = 50
    values = []

    print('Solution...')

    for tick in range(1, steps+1):
        print(f'-> Step {tick}')
        new_pic = defaultdict(int)
        
        min_i, min_j, max_i, max_j = None, None, None, None
    
        for pixel in pic:
            i, j = pixel[0], pixel[1]
            if min_i is None or i < min_i:
                min_i = i
            if min_j is None or j < min_j:
                min_j = j
            if max_i is None or i > max_i:
                max_i = i
            if max_j is None or j > max_j:
                max_j = j

        for i in range(min_i-PADDING, max_i+PADDING):
            for j in range(min_j-PADDING, max_j+PADDING):
                current = (i, j)
                position = ''
                for offset in NEIGHBORS:
                    neighbor = (current[0]+offset[0], current[1]+offset[1])
                    px = pic.get(neighbor, 0 if tick % 2 else 1)
                    position += str(px)
                position = int(position,2)
                new_pic[(i,j)] = decode_pixel(position, codec)
        pic = new_pic
        
        if tick == 2 or tick == 50: values.append(sum(pic.values()))
    
    print(f'\nAfter 2 enhancements: {values[0]} pixels. After 50 enhanceents: {values[-1]} pixels.')
