from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, IntEnum, unique
from functools import reduce, cache
import itertools
from operator import mul
from typing import Any, Iterator, Type, TypeVar, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.Geometry.PointTransforms import Direction2, DirectionsCharset_T
from AOC_Lib.Geometry.LineSegment import Segment2_DiscreteAA


@unique
class TileType(Enum):
    EMPTY = "empty"
    SAND = "sand"
    ROCK = "rock"


class BreakContinue(Exception):
    pass


class Solution_2022_14(SolutionBase):
    """https://adventofcode.com/2022/day/14"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.rock_tiles: set[DiscretePoint2] = set()
        self.sand_tiles: set[DiscretePoint2] = set()

        for line in self.input_str_list(include_empty_lines=False):
            point_strs = line.split("->")

            points = list(
                map(
                    lambda x: DiscretePoint2(*map(int, x.strip().split(","))),
                    point_strs,
                )
            )

            a, b = itertools.tee(points)
            next(b)

            for u, v in zip(a, b):
                segment = Segment2_DiscreteAA(u, v)
                for point in segment.iter_points():
                    self.rock_tiles.add(point)
        print(self.rock_tiles)

    def _is_open_tile(self, pos: DiscretePoint2) -> bool:
        return (pos not in self.rock_tiles) and (pos not in self.sand_tiles)

    def _add_one_sand(
        self,
        pos: DiscretePoint2 = DiscretePoint2(500, 0),
    ) -> Optional[DiscretePoint2]:
        """Add one sand starting at `pos` and simulate falling

        Note: gravity is applied (the down direction) to positive y

        Returns the position at which the sand comes to rest, or `None` if it falls out of the map
        """
        last_rock_y = max(map(lambda p: p.y, self.rock_tiles)) + 2

        while pos.y <= last_rock_y:

            try:
                for t in [
                    DiscretePoint2(0, 1),
                    DiscretePoint2(-1, 1),
                    DiscretePoint2(1, 1),
                ]:
                    new_pos = pos + t
                    if self._is_open_tile(new_pos):
                        pos = new_pos
                        raise BreakContinue
            except BreakContinue:
                continue

            # The sand has come to rest
            self.sand_tiles.add(pos)
            return pos
        return None

    def _smart_add_sand(
        self,
        entry_pos: DiscretePoint2 = DiscretePoint2(500, 0),
    ) -> Optional[DiscretePoint2]:
        """Add sand until one falls out the bottom or the `entry_pos` position is placed

        Returns `None` if sand falls out the bottom
        Otherwise returns the last placed position (which should be `entry_pos`)
        """

        last_rock_y = max(map(lambda p: p.y, self.rock_tiles)) + 2

        positions: list[DiscretePoint2] = []
        positions.append(entry_pos)

        while positions:
            this_pos = positions[-1]

            if not self._is_open_tile(this_pos):
                assert this_pos != entry_pos
                positions.pop()
                continue

            if this_pos.y > last_rock_y:
                # We have fallen out the bottom
                return None

            try:
                for t in [
                    DiscretePoint2(0, 1),
                    DiscretePoint2(-1, 1),
                    DiscretePoint2(1, 1),
                ]:
                    new_pos = this_pos + t
                    if self._is_open_tile(new_pos):
                        positions.append(new_pos)
                        raise BreakContinue
            except BreakContinue:
                continue

            # The sand has come to rest
            self.sand_tiles.add(this_pos)
            positions.pop()
            if this_pos == entry_pos:
                return entry_pos
            else:
                continue
        raise RuntimeError("Neither end condition was met")

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        r = self._smart_add_sand()
        assert r is None
        return len(self.sand_tiles)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        last_rock_y = max(map(lambda p: p.y, self.rock_tiles)) + 2

        seg = Segment2_DiscreteAA(
            DiscretePoint2(-100, last_rock_y),
            DiscretePoint2(1100, last_rock_y),
        )

        for pt in seg.iter_points():
            assert self._is_open_tile(pt)
            self.rock_tiles.add(pt)

        # Doing this would be detrimental
        # self.sand_tiles = set()

        r = self._smart_add_sand()
        assert r is not None
        return len(self.sand_tiles)
