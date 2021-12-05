from testfixtures import compare

from day04.day04 import load_calls_and_boards, get_winning_number_and_score, has_won, mark_number_as_none, \
    sum_remaining_numbers, get_worst_board_winning_number_and_score


def test_load_calls_and_boards():
    calls, boards = load_calls_and_boards("day04_test_data.txt")
    expected_calls = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    expected_boards = [
        [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]],
        [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]],
        [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]],
    ]
    compare(expected_calls, actual=calls)
    compare(expected_boards, actual=boards)


def test_has_won():
    winning_row = [[None, None, None, None, None], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5],
                   [1, 12, 20, 15, 19]]
    winning_col = [[None, 13, 17, 11, 0], [None, 2, 23, 4, 24], [None, 9, 14, 16, 7], [None, 10, 3, 18, 5],
                   [None, 12, 20, 15, 19]]
    not_won = [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    compare(True, has_won(winning_col))
    compare(True, has_won(winning_row))
    compare(False, has_won(not_won))


def test_mark_number_as_none():
    board = [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    expected = [[None, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    compare(expected, actual=mark_number_as_none(22, board))


def test_sum_remaining_numbers():
    board = [[None, None, None, None, None], [8, None, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5]]
    compare(168, actual=sum_remaining_numbers(board))


def test_calculate_winning_number_and_score():
    calls, boards = load_calls_and_boards("day04_test_data.txt")
    winning_number, board_score = get_winning_number_and_score(calls, boards)
    compare(24, actual=winning_number)
    compare(188, actual=board_score)

def test_calculate_worst_board_winning_number_and_score():
    calls, boards = load_calls_and_boards("day04_test_data.txt")
    winning_number, board_score = get_worst_board_winning_number_and_score(calls, boards)
    compare(13, actual=winning_number)
    compare(148, actual=board_score)
