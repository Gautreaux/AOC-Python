
import itertools
from typing import Optional


from AOC_Lib.SlidingWindow import batched
from AOC_Lib.SolutionBase import SolutionBase, Answer_T


class Solution_2022_03(SolutionBase):
    """https://adventofcode.com/2022/day/3"""

    @classmethod
    def get_priority(cls, c: str) -> int:
        """Return the priority for this item"""
        if c == c.upper():
            return ord(c) - ord('A') + 27
        else:
            return ord(c) - ord('a') + 1

    def _part_1_hook(self) -> Optional[Answer_T]:

        self.rucksacks: list[str] = []

        for line in self.input_str_list(include_empty_lines=False):
            i = len(line)
            lhs = line[:i//2]
            rhs = line[i//2:]

            self.rucksacks.append((lhs, rhs))

        return sum(
            map(
                lambda x: self.get_priority(x),
                itertools.chain.from_iterable(map(
                    lambda x: set(x[0]).intersection(x[1]),
                    self.rucksacks,
                ))
            )
        )

    def _part_2_hook(self) -> Optional[Answer_T]:

        return sum(
            map(
                lambda x: self.get_priority(x),
                itertools.chain.from_iterable(map(
                    lambda x: set(x[0]).intersection(x[1]).intersection(x[2]),
                    batched(self.input_str_list(), 3)
                ))
            )
        )
