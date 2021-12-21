from collections import defaultdict
from random import random


class Die:
    def __init__(self) -> None:
        super().__init__()
        self.rolls_so_far = 0

    def roll(self):
        raise NotImplementedError


class DeterministicDie(Die):

    def __init__(self) -> None:
        super().__init__()

    def roll(self):
        self.rolls_so_far += 1
        return (self.rolls_so_far - 1) % 100 + 1  # wrap at 100


class Player:

    def __init__(self, starting_position=None) -> None:
        super().__init__()
        assert starting_position is None or 1 <= starting_position <= 10
        self.board_position = int(random() * 10) + 1 if starting_position is None else starting_position
        self.score = 0

    def move(self, places):
        self.board_position += places % 10
        self.board_position = self.board_position - 10 if self.board_position > 10 else self.board_position
        self.score += self.board_position


def roll_to_win(player1, player2, die):
    while True:
        for player in player1, player2:
            player.move(die.roll() + die.roll() + die.roll())
            if player.score >= 1000:
                return player1, player2, die


def roll_to_win_dirac(player1_start_position=8, player2_start_position=5):
    p1_wins = 0
    p2_wins = 0

    def move(player, places):
        board_position, score = player
        board_position += places % 10
        board_position = board_position - 10 if board_position > 10 else board_position
        score += board_position
        return board_position, score

    # player ==  (position, score)  ... not using objects so that I can index/count them more easily
    players2universes = {((player1_start_position, 0), (player2_start_position, 0)): 1}
    # three rolls of the dirac die have the following outcomes {sum of three rolls: times it happens}
    roll2count = {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}

    while players2universes:  # keep rollin'
        # Player 1's Turn
        new = defaultdict(int)
        for roll, count in roll2count.items():
            for (p1, p2), universes in players2universes.items():
                p1_new = move(p1, roll)
                new[(p1_new, p2)] += (count * universes)
        p1_wins += sum([count for (p1, p2), count in new.items() if p1[1] >= 21])
        players2universes = {(p1, p2): count for (p1, p2), count in new.items() if p1[1] < 21}

        # Player 2's Turn
        new = defaultdict(int)
        for roll, count in roll2count.items():
            for (p1, p2), universes in players2universes.items():
                p2_new = move(p2, roll)
                new[(p1, p2_new)] += (count * universes)
        p2_wins += sum([count for (p1, p2), count in new.items() if p2[1] >= 21])
        players2universes = {(p1, p2): count for (p1, p2), count in new.items() if p2[1] < 21}

    return p1_wins, p2_wins


if __name__ == '__main__':
    die = DeterministicDie()
    player1 = Player(starting_position=8)
    player2 = Player(starting_position=5)
    player1, play2, die = roll_to_win(player1, player2, die)
    losing_score = min(player1.score, player2.score)
    print(f"The final metric is: {losing_score * die.rolls_so_far}")

    p1wins, p2wins = roll_to_win_dirac(player1_start_position=8, player2_start_position=5)
    print(f"After rolling the dirac dice, p1 wins {p1wins} and p2 wins {p2wins}")
