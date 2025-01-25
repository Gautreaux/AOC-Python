from dataclasses import dataclass, field
from typing import Optional


from AOC_Lib.Geometry.LineSegment import Segment2_DiscreteAA, DegenerateMultipoint
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class ElfRange:

    low: int
    high: int

    _segment: Segment2_DiscreteAA = field(default=None, init=False)

    def __post_init__(self):
        self._segment = Segment2_DiscreteAA(
            DiscretePoint2(self.low, 0),
            DiscretePoint2(self.high, 0),
        )

    @classmethod
    def from_str(cls, s: str) -> "ElfRange":
        """From the #-# format"""
        a, _, b = s.partition("-")
        l = min(int(a), int(b))
        u = max(int(a), int(b))
        return cls(low=l, high=u)

    def contains(self, other: "ElfRange") -> bool:
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other: "ElfRange") -> bool:
        try:
            return self._segment.get_intersection(other._segment) is not None
        except DegenerateMultipoint:
            return True


class Solution_2022_04(SolutionBase):
    """https://adventofcode.com/2022/day/4"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        p1_counter = 0
        p2_counter = 0

        for line in self.input_str_list(include_empty_lines=False):
            r1, _, r2 = line.partition(",")

            elf1 = ElfRange.from_str(r1)
            elf2 = ElfRange.from_str(r2)

            if elf1.contains(elf2) or elf2.contains(elf1):
                p1_counter += 1
            if elf1.overlaps(elf2):
                p2_counter += 1
        self._part_1_answer = p1_counter
        self._part_2_answer = p2_counter
