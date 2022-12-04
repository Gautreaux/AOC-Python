

from typing import Optional


from AOC_Lib.Geometry.LineSegment import Segment2_DiscreteAA
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T



class Elf:


    def __init__(self, range: str) -> None:
        a,_,b = range.partition('-')
        self.low = min(int(a), int(b))
        self.high = max(int(a), int(b))

    def contains(self, other: 'Elf') -> bool:
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other: 'Elf') -> bool:
        if self.low in range(other.low, other.high+1):
            return True
        if self.high in range(other.low, other.high+1):
            return True
        if other.low in range(self.low, self.high+1):
            return True
        if other.high in range(self.low, self.high+1):
            return True
        return False

class Solution_2022_04(SolutionBase):
    """https://adventofcode.com/2022/day/4"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        for line in self.input_str_list(include_empty_lines=False):
            pass

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        counter = 0

        counter_2 = 0

        for line in self.input_str_list(include_empty_lines=False):
            r1, _, r2 = line.partition(',')

            elf1 = Elf(r1)
            elf2 = Elf(r2)

            if elf1.contains(elf2) or elf2.contains(elf1):
                counter += 1

            if elf1.overlaps(elf2):
                counter_2 += 1

        self._part_2_answer = counter_2
            
        return counter


    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
