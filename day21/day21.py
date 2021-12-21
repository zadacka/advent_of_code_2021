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
        return self.rolls_so_far


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


if __name__ == '__main__':
    die = DeterministicDie()
    # Player 1 starting position: 8
    # Player 2 starting position: 5
    player1 = Player(8)
    player2 = Player(5)
    player1, play2, die = roll_to_win(player1, player2, die)
    losing_score = min(player1.score, player2.score)
    print(f"The final metric is: {losing_score * die.rolls_so_far}")