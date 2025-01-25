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


class Solution_2022_12(SolutionBase):
    """https://adventofcode.com/2022/day/12"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.area_map: dict[DiscretePoint2, int] = {}
        self.start_pos = DiscretePoint2(-1, -1)
        self.end_pos = DiscretePoint2(-1, -1)

        for y, line in enumerate(self.input_str_list()):
            for x, cell in enumerate(line):
                if cell == "S":
                    self.start_pos = DiscretePoint2(x, y)
                    cell = "a"
                elif cell == "E":
                    self.end_pos = DiscretePoint2(x, y)
                    cell = "z"
                self.area_map[DiscretePoint2(x, y)] = ord(cell) - ord("a")

        assert all(map(lambda x: x >= 0 and x < 26, self.area_map.values()))
        assert self.start_pos.x >= 0
        assert self.end_pos.x >= 0

    def find_steps_to_end_pos(
        self, start_pos: DiscretePoint2, cull_at: Optional[int] = None
    ) -> Optional[int]:
        """Find the number of steps from the supplied `start_pos` to the `end_pos`
        Terminate the search if no path is found in less than `cull_at` steps
        """

        frontier: deque[tuple[DiscretePoint2, int]] = deque()
        frontier.append((start_pos, 0))

        visited: set[DiscretePoint2] = set()

        while frontier:
            this_pos, this_dist = frontier.popleft()

            if cull_at and this_dist > cull_at:
                return None

            if this_pos == self.end_pos:
                return this_dist

            if this_pos in visited:
                continue
            visited.add(this_pos)

            this_elevation = self.area_map[this_pos]
            for neighbor_pos in this_pos.cartesian_neighbors():
                if neighbor_pos in visited:
                    continue
                try:
                    neighbor_elevation = self.area_map[neighbor_pos]
                except KeyError:
                    # Outside the map
                    continue

                if neighbor_elevation - this_elevation <= 1:
                    frontier.append((neighbor_pos, this_dist + 1))
        return None

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        a = self.find_steps_to_end_pos(self.start_pos)
        assert a != None
        return a

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        all_pos_height_a = map(
            lambda x: x[0],
            filter(
                lambda x: x[1] == 0,
                self.area_map.items(),
            ),
        )

        def none_min(a, b):
            return a if b is None else (b if a is None else min(a, b))

        def reducer(i, p):
            return none_min(i, self.find_steps_to_end_pos(p, cull_at=i))

        return reduce(
            reducer,
            all_pos_height_a,
            None,
        )
