import os
import numpy as np
from time import sleep

print('Day 11 of Advent of Code!')

ADJACENT = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
FLASHPOINT = 9

ANIMATION_STEP = 0.25
ANIMATION_OCTOPUS = '@'
ANIMATION_COLORS = {}
for value, color in enumerate(range(237, 247)):
    ANIMATION_COLORS[value] = color
ANIMATION_GLOW = 118
#color tester
#for i in range(256): print(f'\x1b[38;5;{i}m' + f'{i}')

class Game:
    def __init__(self, data: str) -> None:
        self.board = []
        self.ticks = 0
        self.flashes = 0
        self.after_hundred = None
        self.first_synchro = None

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
                octopus._find_neighbors(self)

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
        return [octopus for line in self.board for octopus in line if not octopus.flashing and octopus.is_loaded()]

    def _flash_all_ready(self, to_flash) -> None:
        for octopus in to_flash:
            octopus.flash()
            self.flashes += 1

    def _reset_all_ready(self) -> None:
        for line in self.board:
            for octopus in line:
                if octopus.flashing and octopus.is_loaded():
                    octopus.reset()

    def _find_synchro_flash(self) -> bool:
        return sum(octopus.value for line in self.board for octopus in line) == 0

    def step(self, with_vis=False, vis_with_numbers=False) -> None:
        self._increment_all()
        to_flash = self._find_ready_to_flash()

        while to_flash:
            self._flash_all_ready(to_flash)
            to_flash = self._find_ready_to_flash()

        if with_vis:
            print('\n\n')
            self.draw_board(vis_with_numbers)
            info = f'\x1b[0mSteps: {self.ticks}\nFlashes: {self.flashes}\n'
            info += f'Flashes after 100 steps: {self.after_hundred if self.after_hundred else "Not yet reached!"}\n'
            info += f'First synchro: {self.first_synchro if self.first_synchro else "Not yet!"}'
            print(info)
            sleep(ANIMATION_STEP)
            print("\033[F"*20)

        self._reset_all_ready()
        self.ticks += 1

    def draw_board(self, vis_with_numbers=False) -> None:
        draw = [[octopus.get_colored_octopus(vis_with_numbers) for octopus in line] for line in self.board]
        for line in draw:
            print(''.join(line))

    def run_simulation(self, steps, with_vis=False, vis_with_numbers=False) -> None:
        for i in range(steps+1):
            self.step(with_vis, vis_with_numbers)

            if with_vis and self.ticks <= steps:
                os.system("cls") if os.name == "nt" else os.system("clear")

            if self.ticks == 100:
                self.after_hundred = self.flashes

            if not self.first_synchro and self._find_synchro_flash():
                self.first_synchro = self.ticks


class Octopus:
    def __init__(self, i, j, board: list) -> None:
        self.y = i
        self.x = j
        self.flashing = False
        self.value = board[i][j]
        self.neighbors = []

    def _find_neighbors(self, game: Game) -> None:
        for location in ADJACENT:
            dy, dx = location[0], location[1]
            new_y = self.y + dy
            new_x = self.x + dx
            if 0 <= new_x < game.width and 0 <= new_y < game.height:
                self.neighbors.append(game.board[new_y][new_x])

    def is_loaded(self) -> bool:
        return self.value > FLASHPOINT

    def increment(self) -> None:
        self.value += 1

    def flash(self) -> None:
        self.flashing = True
        for neighbor in self.neighbors:
            neighbor.increment()

    def reset(self) -> None:
        self.flashing = False
        self.value = 0

    def __repr__(self) -> str:
        return str(self.value)

    def get_colored_octopus(self, vis_with_numbers=False) -> str:
        octopus = ANIMATION_OCTOPUS
        if vis_with_numbers and not self.flashing:
            octopus = str(self.value)
        if self.flashing:
            return f'\x1b[38;5;{ANIMATION_GLOW}m' + octopus
        else:
            return f'\x1b[38;5;{ANIMATION_COLORS[self.value]}m' + octopus
                

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

with open('inp', mode='r') as inp:
    raw_data = inp.read()
    G = Game(raw_data.splitlines())
    with_vis, vis_with_numbers = True, False
    G.run_simulation(600, with_vis, vis_with_numbers)
    print(f'{G.after_hundred} flashes after 100 steps, first synchro after {G.first_synchro}.')
