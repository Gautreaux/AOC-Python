from dataclasses import dataclass
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class OasisHistory:
    """Map the readings of OASIS History"""

    readings: tuple[int, ...]

    @staticmethod
    def parse(line: str) -> "OasisHistory":
        """Parse from the line of ints"""
        return OasisHistory(tuple(map(int, line.split(" "))))

    @staticmethod
    def _extrapolate(readings: tuple[int, ...]) -> tuple[int, ...]:
        """Extrapolate the next reading and return the new history"""
        if len(readings) <= 1:
            # Assuming in this case we return (0,0), but not sure
            raise RuntimeError("Readings length is <= 1")

        if all(r == 0 for r in readings):
            return tuple([0] * (len(readings) + 1))

        # compute the down difference
        down_diff = tuple(b - a for a, b in itertools.pairwise(readings))
        res = OasisHistory._extrapolate(down_diff)

        new_value = res[-1] + readings[-1]
        return tuple(itertools.chain(readings, [new_value]))

    @staticmethod
    def _extrapolate_backwards(readings: tuple[int, ...]) -> tuple[int, ...]:
        """Extrapolate the readings backwards"""
        if len(readings) <= 1:
            # Assuming in this case we return (0,0), but not sure
            raise RuntimeError("Readings length is <= 1")

        if all(r == 0 for r in readings):
            return tuple([0] * (len(readings) + 1))

        # compute the down difference
        down_diff = tuple(b - a for a, b in itertools.pairwise(readings))
        res = OasisHistory._extrapolate_backwards(down_diff)

        new_value = readings[0] - res[0]
        return tuple(itertools.chain([new_value], readings))

    def extrapolate(self) -> "OasisHistory":
        """Extrapolate the next reading and return the new history"""
        return OasisHistory(self._extrapolate(self.readings))

    def extrapolate_backwards(self) -> "OasisHistory":
        """Extrapolate the prior reading and return the new history"""
        return OasisHistory(self._extrapolate_backwards(self.readings))


class Solution_2023_09(SolutionBase):
    """https://adventofcode.com/2023/day/9"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.histories: list[OasisHistory] = [
            OasisHistory.parse(l) for l in self.input_str_list()
        ]

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        extrapolated = [h.extrapolate() for h in self.histories]
        return sum(h.readings[-1] for h in extrapolated)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        extrapolated = [h.extrapolate_backwards() for h in self.histories]
        return sum(h.readings[0] for h in extrapolated)
