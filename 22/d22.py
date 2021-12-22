import re

print('Day 22 of Advent of Code!')

REGEX = r'(\w+) x=(-?[\d]+)..(-?[\d]+),y=(-?[\d]+)..(-?[\d]+),z=(-?[\d]+)..(-?[\d]+)'
ON = 'on'
OFF = 'off'

def get_commands(data):
    commands = []
    for line in data.splitlines():
        parsed = re.findall(REGEX, line)[0]
        cmd_type = parsed[0]
        x1, x2 = int(parsed[1]), int(parsed[2])
        y1, y2 = int(parsed[3]), int(parsed[4])
        z1, z2 = int(parsed[5]), int(parsed[6])
        command = {'TYPE': cmd_type, 'X': (x1, x2), 'Y': (y1, y2), 'Z': (z1, z2)}
        commands.append(command)
    return commands


def part1(data):

    def check_range(cmd):
        xs, ys, zs = cmd['X'], cmd['Y'], cmd['Z']
        return xs[0] >= -50 and xs[1] <= 50 and ys[0] >= -50 and ys[1] <= 50 and zs[0] >= -50 and zs[1] <= 50

    cubes = set()
    cmds = get_commands(data)

    for c in cmds:
        if check_range(c):
            for x in range(c['X'][0],c['X'][1]+1):
                for y in range(c['Y'][0],c['Y'][1]+1):
                    for z in range(c['Z'][0],c['Z'][1]+1):
                        cube = (x, y, z)
                        if c['TYPE'] == ON and cube not in cubes:
                            cubes.add(cube)
                        elif c['TYPE'] == OFF and cube in cubes:
                            cubes.remove(cube)
    return len(cubes)

def get_intersect_coordinates(this_coords, other_coords):
    def get_intersect_range(this_min, this_max, other_min, other_max):
        if other_min > this_max or this_min > other_max:
            # e.g. for X: first condition is 'other is too far right', second is 'this is too far right'
            return None
        else:
            # the intersection - if it occurs - is always between the smaller max and bigger min, i.e. the 'mid' values!
            # need to sort them because we don't know the 'side' on which the intersect occurs

            sorted_vals = sorted([this_min, this_max, other_min, other_max])
            return sorted_vals[1], sorted_vals[2]

    this_x, this_X, this_y, this_Y, this_z, this_Z = this_coords
    other_x, other_X, other_y, other_Y, other_z, other_Z = other_coords
    
    intersect_xs = get_intersect_range(this_x, this_X, other_x, other_X)
    intersect_ys = get_intersect_range(this_y, this_Y, other_y, other_Y)
    intersect_zs = get_intersect_range(this_z, this_Z, other_z, other_Z)
    
    all_intersects = [intersect_xs, intersect_ys, intersect_zs]
    
    return all_intersects if all(all_intersects) else None # three tuples or nothing

class Cuboid:
    def __init__(self, x, X, y, Y, z, Z):
        self.coords = (x, X, y, Y, z, Z)
        self.hollows = []
    
    def __repr__(self):
        x, X, y, Y, z, Z = self.coords
        status = f'Cuboid: Xs {x}-{X}, Ys {y}-{Y}, Zs {z}-{Z}. Empty spaces inside: {len(self.hollows)}. Volume: {self.volume()}'
        return status

    def remove_intersection(self, other):
        intersection_coords = get_intersect_coordinates(self.coords, other)
        if not intersection_coords:
            #print('No intersection!')
            return
        else:
            x_, X_ = intersection_coords[0][0], intersection_coords[0][1]
            y_, Y_ = intersection_coords[1][0], intersection_coords[1][1]
            z_, Z_ = intersection_coords[2][0], intersection_coords[2][1]

            for hollow_cube in self.hollows: # clear existing internal 'vacuum' spaces
                hollow_cube.remove_intersection((x_, X_, y_, Y_, z_, Z_))
            
            #print(f'Adding hollow cube', (x_, X_, y_, Y_, z_, Z_))

            self.hollows.append(Cuboid(x_, X_, y_, Y_, z_, Z_)) # and add a new 'vacuum' once!
    
    def volume(self):
        x, X, y, Y, z, Z = self.coords
        return (X - x + 1) * (Y - y + 1) * (Z - z + 1) - sum(hollow_cube.volume() for hollow_cube in self.hollows)

def part2(data):
    all_cuboids = []
    commands = get_commands(data)

    for cmd in commands:
        #print(f'**** Executing: {cmd}')
        cmd_type = cmd['TYPE']
        x, X, y, Y, z, Z = cmd['X'][0], cmd['X'][1], cmd['Y'][0], cmd['Y'][1], cmd['Z'][0], cmd['Z'][1]
        for cuboid in all_cuboids:
            #print(f'Removing intersections...')
            cuboid.remove_intersection((x, X, y, Y, z, Z))
            
        if cmd_type == ON:
            #print(f'Adding new cube', (x, X, y, Y, z, Z))
            all_cuboids.append(Cuboid(x, X, y, Y, z, Z))

    return sum(cuboid.volume() for cuboid in all_cuboids)


raw_data = '''on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507'''

print('Tests...')
print('After initialization procedure:', part1(raw_data) == 474140)
print('After full reboot:', part2(raw_data) == 2758514936282235)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print('After initialization procedure:', part1(raw_data))
    print('After full reboot:', part2(raw_data))
    
    