'''
#############
#12.3.4.5.67#
###1#2#3#4###
  # # # # #
  # # # # #
  # # # # #
  #########

POKOJE: 11, 12, 13, 14 (A, B, C, D)
'''

MAZE = '##############...........####.#.#.#.###  # # # # #    # # # # #    # # # # #    #########'

STR_LOCS = {1: [14], 2: [15], 3: [17], 4: [19], 5: [21], 6: [23], 7: [24], 
11: [68, 55, 42, 29], 
12: [70, 57, 44, 31],
13: [72, 59, 46, 33],
14: [74, 61, 48, 35]}

A, B, C, D = 'A', 'B', 'C', 'D'
COPIES = 4
ALL_AMPHIPODS = [A] * COPIES + [B] * COPIES + [C] * COPIES + [D] * COPIES

CORRIDORS = {1, 2, 3, 4, 5, 6, 7}
ROOMS = {11, 12, 13, 14}

MOVE_COSTS = {A: 1, B: 10, C: 100, D: 1000}

categories_to_rooms = {A: 11, B: 12, C: 13, D: 14}

corridor_to_room = { #(from, to): (moves, [through what])
    (1,11): (3, [2]),
    (1,12): (5, [2,3]),
    (1,13): (7, [2,3,4]),
    (1,14): (9, [2,3,4,5]),
    (2,11): (2, []),
    (2,12): (4, [3]),
    (2,13): (6, [3,4]),
    (2,14): (8, [3,4,5]),
    (3,11): (2, []),
    (3,12): (2, []),
    (3,13): (4, [4]),
    (3,14): (6, [4,5]),
    (4,11): (4, [3]),
    (4,12): (2, []),
    (4,13): (2, []),
    (4,14): (4, [5]),
    (5,11): (6, [3,4]),
    (5,12): (4, [4]),
    (5,13): (2, []),
    (5,14): (2, []),
    (6,11): (8, [3,4,5]),
    (6,12): (6, [4,5]),
    (6,13): (4, [5]),
    (6,14): (2, []),
    (7,11): (9, [3,4,5,6]),
    (7,12): (7, [4,5,6]),
    (7,13): (5, [5,6]),
    (7,14): (3, [6])
}

room_to_corridor = { #(from, to): (moves, [through what])
    (11,1): (3, [1,2]),
    (11,2): (2, [2]),
    (11,3): (2, [3]),
    (11,4): (4, [3,4]),
    (11,5): (6, [3,4,5]),
    (11,6): (8, [3,4,5,6]),
    (11,7): (9, [3,4,5,6,7]),
    (12,1): (5, [1,2,3]),
    (12,2): (4, [2,3]),
    (12,3): (2, [3]),
    (12,4): (2, [4]),
    (12,5): (4, [4,5]),
    (12,6): (6, [4,5,6]),
    (12,7): (7, [4,5,6,7]),
    (13,1): (7, [1,2,3,4]),
    (13,2): (6, [2,3,4]),
    (13,3): (4, [3,4]),
    (13,4): (2, [4]),
    (13,5): (2, [5]),
    (13,6): (4, [5,6]),
    (13,7): (5, [5,6,7]),
    (14,1): (9, [1,2,3,4,5]),
    (14,2): (8, [2,3,4,5]),
    (14,3): (6, [3,4,5]),
    (14,4): (4, [4,5]),
    (14,5): (2, [5]),
    (14,6): (2, [6]),
    (14,7): (3, [6,7])
}

class Location:
    def __init__(self, id):
        self.id = id
        self.amphipods = []
        self.categories = set()

    def __repr__(self):
        return f'ID: {self.id}. Amphipods: {self.amphipods}'

    def copy(self):
        new = Location(self.id)
        new.amphipods = self.amphipods.copy()
        new.categories = self.categories.copy()
        return new

    def has_only_proper(self):
        if not self.amphipods:
            return False

        for amphipod in self.amphipods:
            if amphipod.category not in self.categories:
                return False
        return True

    def is_full(self):
        if self.id < 10:
            return len(self.amphipods) >= 1
        elif self.id > 10:
            return len(self.amphipods) >= 4

    def is_empty(self):
        return not self.amphipods

    def add_amphipod(self, amphipod):
        if not self.is_full():
            self.amphipods.append(amphipod)
    
    def get_next(self):
        if not self.is_empty():
            return self.amphipods.pop()

    def peek_next(self):
        if not self.is_empty():
            return self.amphipods[-1]

class Amphipod:
    def __init__(self, category):
        self.category = category
        self.moves = 0
    
    def __repr__(self):
        return str(self.category)

class State:
    def __init__(self, corridors: list, rooms: list, cost=0):
        self.corridors = {corridor.id: corridor.copy() for corridor in corridors}
        self.rooms = {room.id: room.copy() for room in rooms}
        self.cost = cost

    def __repr__(self):
        return 'S' + str(self.cost)

    def __hash__(self) -> int:
        return hash(self.generate_map())

    def __eq__(self, __o: object) -> bool:
        return self.generate_map() == __o.generate_map()

    def generate_map(self):
        current_maze = list(MAZE)
        for location in self.corridors:
            corridor = self.corridors[location]
            if corridor.amphipods:
                current_maze[STR_LOCS[location][0]] = str(corridor.amphipods[-1])
        for location in self.rooms:
            room = self.rooms[location]
            if room.amphipods:
                to_print = zip(room.amphipods, STR_LOCS[location])
                for amphipod, location in to_print:
                    current_maze[location] = str(amphipod)
        return ''.join(current_maze)
        
    def print(self):
        current_maze = self.generate_map()
        for i in range(0, len(current_maze), 13):
            print(current_maze[i:i+13])

    def find_moves_from_rooms(self):
        moves_to_corridor = []
        
        for room_id in self.rooms:
            room = self.rooms[room_id]
            if room.is_empty() or room.has_only_proper():
                continue
            mover = room.peek_next()
        
            for from_room, to_corridor in room_to_corridor:
                if room.id == from_room:
                    cost, through = room_to_corridor[(from_room, to_corridor)]
                    possible = True
                    for intermediate_area_id in through:
                        if self.corridors[intermediate_area_id].amphipods:
                            possible = False
                            break
                    if possible:
                        moves_to_corridor.append((mover, from_room, to_corridor))
        
        return moves_to_corridor

    def find_moves_to_rooms(self):
        corridors_with_amphipods = []
        moves_to_rooms = []
        
        for corridor_id in self.corridors:
            if self.corridors[corridor_id].amphipods:
                corridors_with_amphipods.append(self.corridors[corridor_id])

        for corridor_area in corridors_with_amphipods:
            mover = corridor_area.peek_next()
            target_room = self.rooms[categories_to_rooms[mover.category]]

            if target_room.is_empty() or target_room.has_only_proper():
                for from_corridor, to_room in corridor_to_room:
                    if corridor_area.id == from_corridor and to_room == target_room.id:
                        cost, through = corridor_to_room[(from_corridor, to_room)]
                        possible = True
                        for intermediate_area_id in through:
                            if self.corridors[intermediate_area_id].amphipods:
                                possible = False
                                break
                        if possible:
                            moves_to_rooms.append((mover, from_corridor, to_room))

        return moves_to_rooms

    def find_moves(self):
        possible_moves = self.find_moves_from_rooms() + self.find_moves_to_rooms()
        if not possible_moves: print("No moves!")
        return possible_moves

    def update_cost(self, mover, moves):
        self.cost += MOVE_COSTS[mover.category] * moves

    def make_move(self, move):
        mover, from_, to = move
        if from_ in self.rooms:
            cost, through = room_to_corridor[(from_, to)]
            mover = self.rooms[from_].get_next()
            self.corridors[to].add_amphipod(mover)
        elif from_ in self.corridors:
            cost, through = corridor_to_room[(from_, to)]
            mover = self.corridors[from_].get_next()
            self.rooms[to].add_amphipod(mover)
        mover.moves += cost
        self.update_cost(mover, cost)

### TRZEBA POPRAWIĆ RUCHY Z POKOJU I DO POKOJU - LICZENIE KOSZTÓW DZIAŁA NIEPRAWIDŁOWO (NIE UWZGLĘDNIA RUCHÓW WEWNĄTRZ POKOJU)
### dodatkowy koszt przy wyjściu/wejściu
### gdy wychodzi: pierwszy wychodzi za 0, drugi za 1, trzeci za 2, czwarty za 3
### gdy wchodzi: pierwszy wchodzi za 3, drugi za 2, trzeci za 1, czwarty za 0
### ZRÓB PARĘ RUCHÓW NA PRÓBĘ
### A POTEM DIJKSTRA ALBO A*


### SETUP OF THE MAZE

corridors = [Location(id) for id in range(min(CORRIDORS),max(CORRIDORS)+1)]
rooms = [Location(id) for id in range(min(ROOMS), max(ROOMS)+1)]
for room, category in zip(rooms, (A, B, C, D)):
    room.categories.add(category)
amphipods = [Amphipod(category) for _, category in enumerate(ALL_AMPHIPODS)]

rooms[0].add_amphipod(amphipods[0])
rooms[0].add_amphipod(amphipods[12])
rooms[0].add_amphipod(amphipods[13])
rooms[0].add_amphipod(amphipods[4])
rooms[1].add_amphipod(amphipods[14])
rooms[1].add_amphipod(amphipods[5])
rooms[1].add_amphipod(amphipods[8])
rooms[1].add_amphipod(amphipods[9])
rooms[2].add_amphipod(amphipods[8])
rooms[2].add_amphipod(amphipods[1])
rooms[2].add_amphipod(amphipods[6])
rooms[2].add_amphipod(amphipods[7])
rooms[3].add_amphipod(amphipods[2])
rooms[3].add_amphipod(amphipods[10])
rooms[3].add_amphipod(amphipods[3])
rooms[3].add_amphipod(amphipods[15])

Game = State(corridors, rooms)


Game.print()
from random import choice
Game.make_move(choice(Game.find_moves()))
Game.print()


print('Day 23 of Advent of Code!')
print('Tests...')
print('---------------------')

print('Solution...')
#with open('inp', mode='r') as inp:
#    raw_data = inp.read()