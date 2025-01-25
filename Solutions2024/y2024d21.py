# from AOC_Lib.name import *
from typing import Iterator
from itertools import permutations


class KeyPad:
    """A Keypad"""

    @staticmethod
    def create_numeric_keypad(self) -> "KeyPad":
        """Create a numeric keypad"""
        values = [
            ("0", (1, 0)),
            ("A", (2, 0)),
            ("1", (0, 1)),
            ("2", (1, 1)),
            ("3", (2, 1)),
            ("4", (0, 2)),
            ("5", (1, 2)),
            ("6", (2, 2)),
            ("7", (0, 3)),
            ("8", (1, 3)),
            ("9", (2, 3)),
        ]
        return KeyPad(values)

    @staticmethod
    def create_direction_keypad(self) -> "KeyPad":
        """Create a direction keypad"""
        values = [
            ("<", (0, 0), "<"),
            ("v", (1, 0), "v"),
            (">", (2, 0), ">"),
            ("^", (1, 1), "^"),
            ("A", (2, 1), "A"),
        ]
        return KeyPad(values)

    @staticmethod
    def _build_strokes_between(
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        valid_posititions: tuple[tuple[int, int]],
    ) -> str:
        """Return the pat to move between these points"""

    def __init__(self, values: Iterator[tuple[str, tuple[int, int]]]):
        self.values: dict[str, tuple[int, int]] = dict(values)

        raise NotImplementedError()


def y2024d21(inputPath=None):
    if inputPath == None:
        inputPath = "Input2024/d21.txt"
    print("2024 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for single line inputs
    for c in lineList[-1]:
        pass

    # for multi line inputs

    return (Part_1_Answer, Part_2_Answer)
