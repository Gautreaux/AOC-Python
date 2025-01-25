# from AOC_Lib.name import *


from dataclasses import dataclass
from typing import Optional
from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass(frozen=True)
class Elf:
    """An Elf, carrying some number of calories"""

    calories_carried: int

    def __lt__(self, other: "Elf") -> bool:
        return self.calories_carried < other.calories_carried


class Solution_2022_01(SolutionBase):
    """https://adventofcode.com/2022/day/1"""

    def __post_init__(self):
        self._elves: list[Elf] = self._load_elves()

    def _load_elves(self) -> list[Elf]:

        elves = []

        t = 0
        for line in self.input_str_list():
            if line:
                t += int(line)
            else:
                elves.append(Elf(t))
                t = 0
        return elves

    def _part_1_hook(self) -> Optional[Answer_T]:
        e: Elf = max(self._elves)
        return e.calories_carried

    def _part_2_hook(self) -> Optional[Answer_T]:
        self._elves.sort()
        return sum(map(lambda x: x.calories_carried, self._elves[-3:]))
