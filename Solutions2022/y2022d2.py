# from AOC_Lib.name import *

from enum import Enum, unique
from typing import Optional

from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@unique
class Action(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def get_action(cls, v: str) -> "Action":
        return {
            "A": cls.ROCK,
            "B": cls.PAPER,
            "C": cls.SCISSORS,
            "X": cls.ROCK,
            "Y": cls.PAPER,
            "Z": cls.SCISSORS,
        }[v]

    @classmethod
    def get_win_outcome(cls, other_move: "Action"):
        return {
            Action.ROCK: Action.PAPER,
            Action.PAPER: Action.SCISSORS,
            Action.SCISSORS: Action.ROCK,
        }[other_move]

    @classmethod
    def get_tie_outcome(cls, other_move: "Action"):
        return other_move

    @classmethod
    def get_loss_outcome(cls, other_move: "Action"):
        return {
            Action.ROCK: Action.SCISSORS,
            Action.SCISSORS: Action.PAPER,
            Action.PAPER: Action.ROCK,
        }[other_move]

    @classmethod
    def get_action_by_outcome(cls, other_move: "Action", desired_outcome: str):
        return {
            "X": cls.get_loss_outcome,
            "Y": cls.get_tie_outcome,
            "Z": cls.get_win_outcome,
        }[desired_outcome](other_move)

    def beats(self, other: "Action") -> bool:
        if self == Action.ROCK and other == Action.SCISSORS:
            return True
        if self == Action.PAPER and other == Action.ROCK:
            return True
        if self == Action.SCISSORS and other == Action.PAPER:
            return True
        return False

    def ties(self, other: "Action") -> bool:
        return self == other


class Solution_2022_02(SolutionBase):
    """https://adventofcode.com/2022/day/2"""

    def score_hand(self, my_move: Action, other_move: Action) -> int:
        if my_move.beats(other_move):
            return 6 + my_move.value
        elif my_move.ties(other_move):
            return 3 + my_move.value
        else:
            return 0 + my_move.value

    def _play_round_p1(self, line: str) -> int:
        o, m = line.split(" ")
        other_move = Action.get_action(o)
        my_move = Action.get_action(m)

        return self.score_hand(my_move, other_move)

    def _play_round_p2(self, line: str) -> int:
        o, m = line.split(" ")
        other_move = Action.get_action(o)
        my_move = Action.get_action_by_outcome(other_move, m)

        return self.score_hand(my_move, other_move)

    def _part_1_hook(self) -> Optional[Answer_T]:
        return sum(self.map_lines(self._play_round_p1))

    def _part_2_hook(self) -> Optional[Answer_T]:
        return sum(self.map_lines(self._play_round_p2))
