import numpy as np

print('Day 11 of Advent of Code!')

ADJACENT = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Game:
    def __init__(self, data: str) -> None:
        self.board = []
        self.ticks = 0
        self.flashes = 0

        for line in data:
            self.board.append(list(map(int, line)))
        
        self.width = len(self.board[0])
        self.height = len(self.board)

        for i in range(self.height):
            for j in range(self.width):
                octopus = Octopus(i, j, self.board)
                self.board[i][j] = octopus        
        
        for line in self.board:
            for octopus in line:
                octopus._find_neighbors(self.board)

        self.board = np.array(self.board)


    def __repr__(self):
        status = f'Game after {self.ticks} steps:\n'
        status += str(self.board)
        status += f'\nFlashes: {self.flashes}'
        status += '\n' + '-' * 20
        return status


    def get_octopus(self, x: int, y: int) -> object:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        else:
            raise IndexError('Location out of bounds!')


    def _increment_all(self) -> None:
        for line in self.board:
            for octopus in line:
                octopus.increment()


    def _find_ready_to_flash(self) -> list:
        to_flash = []
        for line in self.board:
            for octopus in line:
                if not octopus.flashing and octopus.value > 9:
                    to_flash.append(octopus)
        return to_flash


    def _flash_all_ready(self, to_flash) -> None:
        for octopus in to_flash:
            octopus.flash()
            self.flashes += 1


    def _reset_all_ready(self):
        for line in self.board:
            for octopus in line:
                if octopus.flashing and octopus.value > 9:
                    octopus.reset()


    def _find_synchro_flash(self):
        return sum(octopus.value for line in self.board for octopus in line) == 0


    def step(self) -> None:
        self._increment_all()
        to_flash = self._find_ready_to_flash()
        while to_flash:
            self._flash_all_ready(to_flash)
            to_flash = self._find_ready_to_flash()
        self._reset_all_ready()
        if self._find_synchro_flash():
            print(f'Synchronized flash at {self.ticks}!')
        self.ticks += 1


class Octopus:
    def __init__(self, i, j, board) -> None:
        self.y = i
        self.x = j
        self.flashing = False
        self.value = board[i][j]
        self.neighbors = []


    def _find_neighbors(self, board) -> None:
        for location in ADJACENT:
            dy, dx = location[0], location[1]
            new_y = self.y + dy
            new_x = self.x + dx
            if 0 <= new_x < len(board[0]) and 0 <= new_y < len(board):
                self.neighbors.append(board[new_y][new_x])


    def increment(self) -> None:
        self.value += 1


    def flash(self) -> None:
        self.flashing = True
        for neighbor in self.neighbors:
            neighbor.increment()


    def reset(self) -> None:
        self.flashing = False
        self.value = 0
   

    def __repr__(self):
        return str(self.value)


def play_game(game, steps):
    for i in range(steps):
        game.step()
        if game.ticks == 100:
            print(f'After 100 steps: {game.flashes} flashes.')


raw_data = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''


print('Tests...')
G = Game(raw_data.splitlines())
play_game(G, 200)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    G = Game(raw_data.splitlines())
    play_game(G, 550)
