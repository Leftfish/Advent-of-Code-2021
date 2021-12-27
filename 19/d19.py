import re
from copy import copy
from collections import defaultdict, deque
from itertools import product, combinations

print('Day 19 of Advent of Code!')

OVERLAP_THRESHOLD = 11
ROTATIONS = 24

class Scanner:
    # the constructor just gives us a barebones scanner with ID
    # the actual work is done by initiate_scanners() below

    def __init__(self, id: int) -> None:
        self.id = id
        # a list of beacons: tuples with (x, y, z) coordinates
        self.beacons = None
        # vectors from beacon n to all other beacons seen by a scanner
        # a dictionary with beacons (tuples) as keys matched to values: sets of tuples
        self.vectors = None

    def __repr__(self) -> str:
        return f'SCN {self.id}'

    def find_vectors_between_beacons(self) -> None:
        def find_vector(this: tuple, other: tuple) -> tuple:
            x1, y1, z1 = this
            x2, y2, z2 = other
            return ((x2 - x1), (y2 - y1), (z2 - z1))
    
        pairs = combinations(self.beacons, 2)
        vectors = defaultdict(set)

        # this is a crucial part which I overlooked: if we use distances between points
        # to "fingerprint" each scanner, the distance beacon1-beacon2 is the same as
        # for beacon2-beacon1; but if we use vectors, they cannot be the same!

        for one, other in pairs:
            vectors[one].add(find_vector(one, other))
            vectors[other].add(find_vector(other, one))

        self.vectors = vectors

    def rotate(self, i: int) -> None:
        def rotations(beacon, i) -> tuple:
            x, y, z = beacon
            rotates = [(x, y, z),
                (-y, x, z),
                (-x, -y, z),
                (y, -x, z),
                (-z, y, x),
                (-y, -z, x),
                (z, -y, x),
                (y, z, x),
                (-x, y, -z),
                (-y, -x, -z),
                (x, -y, -z),
                (y, x, -z),
                (z, y, -x),
                (-y, z, -x),
                (-z, -y, -x),
                (y, -z, -x),
                (x, -z, y),
                (z, x, y),
                (-x, z, y),
                (-z, -x, y),
                (x, z, -y),
                (-z, x, -y),
                (-x, -z, -y),
                (z, -x, -y)]
            return rotates[i]

        new_beacons = [rotations(beacon, i) for beacon in self.beacons]
        self.beacons = new_beacons
        self.find_vectors_between_beacons()

def initiate_scanners(data: str) -> list:
    regex = r'--- scanner (\d+) ---'
    scanners = []
    beacons = []
    current = None

    for line in data.splitlines():  
        is_new_scanner = re.findall(regex, line)

        if is_new_scanner:
            if current:
                current.beacons = beacons
                beacons = []

            new_scanner = Scanner(int(is_new_scanner[0]))
            scanners.append(new_scanner) 
            current = new_scanner

        elif line:
            beacon = tuple(map(int, line.split(',')))
            beacons.append(beacon)

    current.beacons = beacons

    for scanner in scanners:
        scanner.find_vectors_between_beacons()

    return scanners

def find_overlaps(this_scanner: Scanner, other_scanner: Scanner) -> defaultdict:
    # we compare vectors between beacons (x, y, z) in two scanners
    # if the scanners are aligned properly, i.e. use the same axes, the vectors
    # should be the same for the specified number of beacons
    
    overlaps = defaultdict(set)
    beacon_pairs = product(this_scanner.beacons, other_scanner.beacons)

    for this_beacon, other_beacon in beacon_pairs:
        v_this = this_scanner.vectors[this_beacon]
        v_other = other_scanner.vectors[other_beacon]
        overl = len(v_this & v_other)
        if overl >= OVERLAP_THRESHOLD:
            overlaps[this_beacon].add(other_beacon)
    
    return overlaps

def find_and_normalize(scanners: deque, debug=False) -> tuple:
    # we start with the first scanner, use it as anchor at (0, 0, 0) and build up from it
    # each time a new scanner with overlapping beacons is found, add its beacons to anchor
    # this way we have a growing 'master' scanner (anchor)
    
    anchor = scanners.popleft()
    scanner_coords = {}

    # we take the next scanner from queue and try to align it.

    while scanners:
        tested_scanner = scanners.popleft()
        offset = False
        overlap_found = False
    
        if debug: print(f"Testing anchor ({anchor}) with {len(anchor.beacons)} beacons against {tested_scanner}...")

    # we rotate the scanner popped from the queue up to 24 times to see if it can be matched

        for i in range(ROTATIONS):
            rotated_scanner = copy(tested_scanner)
            rotated_scanner.rotate(i)
            overlaps = find_overlaps(anchor, rotated_scanner)

    # match found? calculate the offset (subtract beacon in scanner A from beacon in scanner B) relative to (0, 0, 0)

            if overlaps:
                overlap_found = True
                this_beacon = list(overlaps.keys())[0]
                other_beacon = overlaps[this_beacon].pop()
                offset = (this_beacon[0]-other_beacon[0], this_beacon[1]-other_beacon[1], this_beacon[2]-other_beacon[2])

    # curiously, the offset is also the location of the scanner that we're now merging!

                scanner_coords[rotated_scanner.id] = offset
    
    # then apply the offset to each beacon in the scanner that is currently tested and now properly rotated
    
                new_beacons = []
                for beacon in rotated_scanner.beacons:
                    x, y, z = beacon
                    ox, oy, oz = offset
                    offset_beacon = (x + ox, y + oy, z + oz)
                    new_beacons.append(offset_beacon)
    
    # now update the list of beacons in the anchor ("master" scanner) and recalculate vectors between its beacons
    # the latter is necessary because the scanner is now larger

                anchor.beacons = list(set(anchor.beacons + new_beacons))
                anchor.find_vectors_between_beacons()
                
                if debug: print(f'Merged! Anchor now has {len(anchor.beacons)} beacons.')

                break

    # no overlap? get that scanner back to the end of the queue    

        if not overlap_found:
            scanners.append(tested_scanner)

    return len(set(anchor.beacons)), scanner_coords

def manhattan(this_scanner_coords: tuple, other_scanner_coords: tuple) -> int:
    x1, y1, z1 = this_scanner_coords
    x2, y2, z2 = other_scanner_coords
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

def find_max_distance(scanner_coords: dict) -> int:
    max_dist = 0
    for this, other in product(scanner_coords, repeat=2):
        dist = manhattan(this, other)
        if dist > max_dist:
            max_dist = dist
    return max_dist

raw_data = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''

print('Tests...')
scanners = deque(initiate_scanners(raw_data))
unique_beacons, scanner_coords = find_and_normalize(scanners, debug=True)
print(f'The field has {unique_beacons} unique beacons. Maximum distance between scanners: {find_max_distance(scanner_coords.values())}.')
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    text = raw_data = inp.read()
    scanners = deque(initiate_scanners(raw_data))
    unique_beacons, scanner_coords = find_and_normalize(scanners)
    print(f'The field has {unique_beacons} unique beacons. Maximum distance between scanners: {find_max_distance(scanner_coords.values())}.')
