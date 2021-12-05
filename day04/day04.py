from copy import deepcopy
from itertools import chain


def load_calls_and_boards(file_name):
    calls = []
    boards = []
    with open(file_name) as f:
        calls = [int(n) for n in f.readline().split(',')]
        next_board = []
        for line in f.readlines():
            if line == '\n':
                continue
            next_board.append([int(n) for n in line.split()])
            if len(next_board) == 5:
                boards.append(next_board)
                next_board = []

    return calls, boards


def mark_number_as_none(called_number, board):
    return [[r if r != called_number else None for r in row] for row in board]


def has_won(board):
    for row in board:
        if all(value is None for value in row):
            return True
    for col in zip(*board):
        if all(value is None for value in col):
            return True
    return False


def sum_remaining_numbers(board):
    return sum(filter(None, chain(*board)))


def get_winning_number_and_score(calls, boards):
    board_index, called_number, remaining_score = get_leaderboard(calls, boards)[0]
    return called_number, remaining_score


def get_worst_board_winning_number_and_score(calls, boards):
    board_index, called_number, remaining_score = get_leaderboard(calls, boards)[-1]
    return called_number, remaining_score


def get_leaderboard(calls, boards):
    b = deepcopy(boards)  # we'll mutate this
    leaderboard = []  # board_index, called_number, sum_of_board
    for called_number in calls:
        for board_index, board in enumerate(b):
            board = mark_number_as_none(called_number, board)
            b[board_index] = board
            if has_won(board) and board_index not in [entry[0] for entry in leaderboard]:
                sum_of_board = sum_remaining_numbers(board)
                leaderboard.append((board_index, called_number, sum_of_board))
            if len(leaderboard) == len(boards):
                # last board has won!
                return leaderboard


if __name__ == "__main__":
    calls, boards = load_calls_and_boards("day04_real_data.txt")

    winning_number, board_score = get_winning_number_and_score(calls, boards)
    msg = "The winning number is {} and the board remaining number sum is {} for a product {}"
    print(msg.format(winning_number, board_score, winning_number * board_score))

    last_winning, last_board_score = get_worst_board_winning_number_and_score(calls, boards)
    msg2 = "The last-to-win board happens when number is {} and the board remaining number sum is {} for a product {}"
    print(msg2.format(last_winning, last_board_score, last_winning * last_board_score))
