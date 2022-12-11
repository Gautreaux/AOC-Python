

from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.Geometry.PointTransforms import Direction2, DirectionsCharset_T


class Santa:

    def __init__(self, start_position: DiscretePoint2 = DiscretePoint2(0,0)) -> None:
        self._pos: DiscretePoint2 = start_position
        self._visited: set[DiscretePoint2] = set()
        self._visited.add(start_position)
    
    @property
    def position(self) -> DiscretePoint2:
        """Get the current position"""
        return self._pos

    @property
    def visited(self) -> set[DiscretePoint2]:
        """Return a set of all visited locations"""
        return self._visited

    def step(self, direction: DirectionsCharset_T) -> None:
        """Step in the provided direction"""
        self._pos = Direction2.transform_point(self._pos, direction)
        self._visited.add(self._pos)


class Solution_2015_03(SolutionBase):
    """https://adventofcode.com/2015/day/3"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        santa = Santa()
        for c in self.input_str():
            santa.step(c) # type: ignore
        return len(santa.visited)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        santa = Santa()
        robosanta = Santa()

        assert len(self.input_str()) % 2 == 0
        itr = iter(self.input_str())
        try:
            while True:
                santa.step(next(itr))  # type: ignore
                robosanta.step(next(itr))  # type: ignore
        except StopIteration:
            pass
        return len(santa.visited.union(robosanta.visited))
