"""https://adventofcode.com/2016/day/2"""

from enum import StrEnum
from AOC_Lib.point import Point2
from AOC_Lib.point import Y_DOWN_2_TRANSFORMS
from AOC_Lib.boundedInt import LockedInt
from AOC_Lib.SolutionBase import SolutionBase


class _LetterKeys(StrEnum):
    """The Keys that are letters"""

    EMPTY = ""
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Solution_2016_02(SolutionBase):
    """https://adventofcode.com/2016/day/2"""

    SIMPLE_KEYPAD = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    COMPLEX_KEYPAD = [
        [_LetterKeys.EMPTY, _LetterKeys.EMPTY, 1, _LetterKeys.EMPTY, _LetterKeys.EMPTY],
        [_LetterKeys.EMPTY, 2, 3, 4, _LetterKeys.EMPTY],
        [5, 6, 7, 8, 9],
        [
            _LetterKeys.EMPTY,
            _LetterKeys.A,
            _LetterKeys.B,
            _LetterKeys.C,
            _LetterKeys.EMPTY,
        ],
        [
            _LetterKeys.EMPTY,
            _LetterKeys.EMPTY,
            _LetterKeys.D,
            _LetterKeys.EMPTY,
            _LetterKeys.EMPTY,
        ],
    ]

    @staticmethod
    def find_keystroke_simple(position: Point2, instructions: str) -> str:
        """Find a keystroke on the simple keypad, update position with the new position"""
        for c in instructions:
            position += Y_DOWN_2_TRANSFORMS[c]

        x: int = position.x.asInt()  # type: ignore
        y: int = position.y.asInt()  # type: ignore
        return str(Solution_2016_02.SIMPLE_KEYPAD[y][x])

    @staticmethod
    def find_keystroke_complex(position: Point2, instructions: str) -> str:
        """Find a keystroke on the complex keypad, update position with the new position"""
        for c in instructions:
            temp_pos = position + Y_DOWN_2_TRANSFORMS[c]

            x: int = temp_pos.x.asInt()  # type: ignore
            y: int = temp_pos.y.asInt()  # type: ignore

            if Solution_2016_02.COMPLEX_KEYPAD[y][x] != _LetterKeys.EMPTY:
                position = temp_pos

        x: int = position.x.asInt()  # type: ignore
        y: int = position.y.asInt()  # type: ignore
        return str(Solution_2016_02.COMPLEX_KEYPAD[y][x])

    def _part_1_hook(self) -> str:
        position = Point2(LockedInt(0, 2, 1), LockedInt(0, 2, 1))
        key_presses = []
        for line in self.input_str_list():
            p = self.find_keystroke_simple(position, line)
            key_presses.append(p)
        return "".join(key_presses)

    def _part_2_hook(self) -> str:
        position = Point2(LockedInt(0, 4, 0), LockedInt(0, 4, 2))
        key_presses = []
        for line in self.input_str_list():
            p = self.find_keystroke_complex(position, line)
            key_presses.append(p)
        return "".join(key_presses)
