print('Day 4 of Advent of Code!')

test_data = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''

def get_moves_and_boards(game: str) -> tuple:
    parsed_game = game.splitlines()
    moves = map(int, parsed_game[0].split(','))
    boards = []
    for line in parsed_game[1:]:
        if not line:
            new_board = list()
            boards.append(new_board)
        else:
            numbers = list(map(int, line.split()))
            new_board.append(numbers)
    return list(moves), boards

def check_win(board: list) -> bool:
    winner = [None for i in range(len(board))]
    for row in board:
        if row == winner:
            return True
    for i in range(len(board)):
        col = [row[i] for row in board]
        if col == winner:
            return True
    return False

def remove_number(board: list, number: int) -> None:
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == number:
                board[i][j] = None
                break

def sum_unmarked_numbers(board: list) -> int:
    score = 0
    for row in board:
        score += sum(number for number in row if number)
    return score

def print_board(board: list) -> None:
    for row in board:
        print(row)
    
def play_round(boards: list, number: int) -> int:
    for board in boards:
        remove_number(board, number)
    
    for board in boards:
        if check_win(board):
            return number * sum_unmarked_numbers(board)
    return 0

def play_bingo(boards: list, moves: list) -> int:
    for move in moves:
        result = play_round(boards, move)
        if result:
            break
    return result

def play_extended_round(boards: list, number: int) -> list:
    winning_boards = []
    print(f"Removing {number}")
    for board in boards:
        remove_number(board, number)
    
    for board in boards:
        if check_win(board):
            winning_boards.append(board)
            print(f"***** after {number}: {board}")

    return winning_boards

def play_extended_bingo(boards: list, moves: list) -> int:
    boards_in_game = boards[:]
    winning_boards = []
    
    for move in moves:
        winning_boards_after_round = play_extended_round(boards_in_game, move)
        for board in winning_boards_after_round:
            boards_in_game.remove(board)
            winning_boards.append((board, move))
    
    return winning_boards


print('Tests...')
moves, boards = get_moves_and_boards(test_data)
#print(play_bingo(boards, moves))
winning = play_extended_bingo(boards, moves)
print(sum_unmarked_numbers(winning[-1][0]) * winning[-1][1])
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    game = inp.read()
    moves, boards = get_moves_and_boards(game)
    #print(play_bingo(boards, moves))
    winning = play_extended_bingo(boards, moves)
    print(sum_unmarked_numbers(winning[-1][0]) * winning[-1][1])

