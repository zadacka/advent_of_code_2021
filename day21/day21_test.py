from testfixtures import compare, ShouldRaise

from day21.day21 import DeterministicDie, Player, roll_to_win, roll_to_win_dirac


def test_deterministic_dice():
    die = DeterministicDie()
    for test_roll in range(1, 101):
        compare(die.roll(), expected=test_roll)

    compare(die.roll(), expected=1)  # should be back to 1 again


def test_player():
    player1 = Player()
    compare(player1.score, expected=0)
    compare(1 <= player1.board_position <= 10, expected=True)

    player1 = Player(9)
    compare(player1.score, expected=0)
    compare(player1.board_position, expected=9)

    player1.move(1)
    compare(player1.score, expected=10)
    compare(player1.board_position, expected=10)

    player1.move(5)
    compare(player1.score, expected=15)
    compare(player1.board_position, expected=5)

    with ShouldRaise(AssertionError):
        invalid_starting_position = 11
        _ = Player(invalid_starting_position)


def test_example():
    player1 = Player(4)
    player2 = Player(8)

    die = DeterministicDie()
    # one
    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(10, 10))
    player2.move(die.roll() + die.roll() + die.roll())
    compare((player2.board_position, player2.score), expected=(3, 3))
    # two
    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(4, 14))
    player2.move(die.roll() + die.roll() + die.roll())
    compare((player2.board_position, player2.score), expected=(6, 9))
    # three
    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(6, 20))
    player2.move(die.roll() + die.roll() + die.roll())
    compare((player2.board_position, player2.score), expected=(7, 16))
    # four
    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(6, 26))
    player2.move(die.roll() + die.roll() + die.roll())
    compare((player2.board_position, player2.score), expected=(6, 22))

    # 993 - 9 - 24 = 960
    for _ in range(160):
        player1.move(die.roll() + die.roll() + die.roll())
        player2.move(die.roll() + die.roll() + die.roll())

    compare(die.rolls_so_far, expected=984)

    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(4, 990))
    player2.move(die.roll() + die.roll() + die.roll())
    compare((player2.board_position, player2.score), expected=(3, 745))

    player1.move(die.roll() + die.roll() + die.roll())
    compare((player1.board_position, player1.score), expected=(10, 1000))  # player 1 wins


def test__get_scores_and_rolls():
    die = DeterministicDie()
    player1 = Player(4)
    player2 = Player(8)
    player1, player2, die = roll_to_win(player1=player1, player2=player2, die=die)
    compare(player1.score, expected=1000)
    compare(player2.score, expected=745)
    compare(die.rolls_so_far, expected=993)


def test_roll_to_win_dirac():
    compare(
        roll_to_win_dirac(player1_start_position=4, player2_start_position=8),
        expected=(444356092776315, 341960390180808)
    )
