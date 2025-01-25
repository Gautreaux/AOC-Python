# from AOC_Lib.name import *

from AOC_Lib.Geometry.DiscreteRegions import DiscreteAABBbounds
from AOC_Lib.Geometry.PointTransforms import Direction2, DirectionsCharset_T
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from typing import Callable, Iterable, Type, TypeVar, Optional
from operator import mul
from functools import reduce, cache
from enum import Enum, IntEnum, unique
from dataclasses import dataclass, field
from collections import defaultdict, deque
import itertools

TOGGLE = 0
TURN_ON = 1
TURN_OFF = 2


def y2015d6(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d6.txt"
    print("2015 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    def parseTuple(tupleStr):
        return tuple(map(int, tupleStr.split(",")))

    instrList = []
    for line in lineList:
        s = line.split(" ")

        if s[0] == "toggle":
            instrList.append(
                (
                    TOGGLE,
                    parseTuple(s[1]),
                    parseTuple(s[-1]),
                )
            )
        else:
            instrList.append(
                (
                    TURN_OFF if s[1] == "off" else TURN_ON,
                    parseTuple(s[2]),
                    parseTuple(s[-1]),
                )
            )

    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    grid2 = [[0 for _ in range(1000)] for _ in range(1000)]

    for instr, left, right in instrList:
        for x in range(left[0], right[0] + 1):
            for y in range(left[1], right[1] + 1):
                if instr == TURN_ON:
                    grid[y][x] = 1
                    grid2[y][x] += 1
                elif instr == TURN_OFF:
                    grid[y][x] = 0
                    grid2[y][x] = max(grid2[y][x] - 1, 0)
                elif instr == TOGGLE:
                    grid[y][x] = 1 if grid[y][x] == 0 else 0
                    grid2[y][x] += 2

    Part_1_Answer = sum(itertools.chain.from_iterable(grid))
    Part_2_Answer = sum(itertools.chain.from_iterable(grid2))

    return (Part_1_Answer, Part_2_Answer)


# ==================


@unique
class _Operation(Enum):
    TURN_OFF = 0
    TURN_ON = 1
    TOGGLE = -1


@dataclass(frozen=True)
class _Instruction:

    operation: _Operation
    corner_a: DiscretePoint2
    corner_b: DiscretePoint2

    @property
    def AABB(self) -> DiscreteAABBbounds:
        """Get the AABB of this instruction"""
        return DiscreteAABBbounds.from_point_set([self.corner_a, self.corner_b])


class Solution_2015_06(SolutionBase):
    """https://adventofcode.com/2015/day/6"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.instructions: list[_Instruction] = []

        for line in self.input_str_list(include_empty_lines=False):
            tokens = line.rsplit(" ", 3)

            op = _Operation[tokens[0].replace(" ", "_").upper()]

            p1 = DiscretePoint2(*map(lambda x: int(x), tokens[1].split(",")))
            p2 = DiscretePoint2(*map(lambda x: int(x), tokens[3].split(",")))

            self.instructions.append(_Instruction(op, p1, p2))

    def _bad_part_1_hook(self):

        # Attempting to use regions to reduce amount of comparisons
        #   but actually much worse
        # and also produces the wrong answer

        pending_regions: dict[DiscreteAABBbounds, Iterable[DiscretePoint2]] = {}

        for i in self.instructions:
            for a, b in itertools.combinations(pending_regions.keys(), 2):
                if a.intersects(b):
                    print("***", a)
                    print("***", b)
                assert not a.intersects(b)

            bounds = DiscreteAABBbounds.from_point_set([i.corner_a, i.corner_b])

            has_intersections = any(
                map(lambda x: bounds.intersects(x), pending_regions.keys())
            )

            if not has_intersections:
                assert not any(
                    map(lambda pr: bounds.intersects(pr), pending_regions.keys())
                )
                print(f"ADD {bounds}")
                if i.operation == _Operation.TURN_ON:
                    # type: ignore
                    pending_regions[bounds] = bounds.generate_bounded_points()
                elif i.operation == _Operation.TURN_OFF:
                    # Nothing to turn off
                    pass
                elif i.operation == _Operation.TOGGLE:
                    # This intersects nothing, all lights start off, so its effectively a turn on
                    # type: ignore
                    pending_regions[bounds] = bounds.generate_bounded_points()
                else:
                    raise NotImplementedError(i.operation)
                continue

            full_bounds: DiscreteAABBbounds = bounds
            existing = iter([])

            found_one_intersection: bool = True
            while found_one_intersection:
                found_one_intersection = False

                for b in pending_regions.keys():
                    if not full_bounds.intersects(b):
                        continue
                    e = pending_regions.pop(b)
                    full_bounds = full_bounds.combine(b)
                    existing = itertools.chain(e, existing)
                    found_one_intersection = True
                    break

            assert not any(
                map(lambda pr: bounds.intersects(pr), pending_regions.keys())
            )
            assert not any(
                map(lambda pr: full_bounds.intersects(pr), pending_regions.keys())
            )
            for a, b in itertools.combinations(pending_regions.keys(), 2):
                if a.intersects(b):
                    print("***", a)
                    print("***", b)
                assert not a.intersects(b)

            if i.operation == _Operation.TURN_ON:
                s = itertools.chain(
                    bounds.generate_bounded_points(),
                    filter(lambda x: not bounds.contains(x), existing),
                )
            elif i.operation == _Operation.TURN_OFF:
                s = filter(lambda x: not bounds.contains(x), existing)
            elif i.operation == _Operation.TOGGLE:
                s = set(existing)
                s.symmetric_difference_update(bounds.generate_bounded_points())
            else:
                raise NotImplementedError(i.operation)

            assert not any(
                map(lambda pr: full_bounds.intersects(pr), pending_regions.keys())
            )
            for a, b in itertools.combinations(pending_regions.keys(), 2):
                if a.intersects(b):
                    print("***", a)
                    print("***", b)
                assert not a.intersects(b)
            print("CMB", full_bounds)
            assert full_bounds not in pending_regions
            pending_regions[full_bounds] = s  # type: ignore
            for a, b in itertools.combinations(pending_regions.keys(), 2):
                if a.intersects(b):
                    print("***", a)
                    print("***", b)
                assert not a.intersects(b)

        print(f"At conclusion, there are {len(pending_regions)} pending regions")

        return len(set(itertools.chain.from_iterable(pending_regions.values())))

    def _part_1_hook_A(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        # Lame iterative way (rather slow)

        on_lights: set[DiscretePoint2] = set()

        for i in self.instructions:
            to_toggle = DiscreteAABBbounds.from_point_set([i.corner_a, i.corner_b])

            if i.operation == _Operation.TURN_ON:
                on_lights.update(to_toggle)  # type: ignore
            elif i.operation == _Operation.TURN_OFF:
                on_lights.difference_update(to_toggle)  # type: ignore
            else:
                on_lights.symmetric_difference_update(to_toggle)  # type: ignore
        return len(on_lights)

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        # Pretty good reverse iterative way
        # Only care about the terminal state
        #   so go reverse and stop tracking points once they are set

        all_bounds = reduce(
            lambda b, x: b.combine(x), map(lambda x: x.AABB, self.instructions)
        )

        normal_points = set(all_bounds.generate_bounded_points())
        toggled_points = set()

        number_on = 0

        for i in reversed(self.instructions):
            print(
                f"{len(normal_points) + len(toggled_points):>10} Remain | {number_on:>9} definitely on| {len(normal_points):>9} points normal | {len(toggled_points):>9} toggled"
            )
            if len(normal_points) == 0 and len(toggled_points) == 0:
                print("No more points, exiting early.")
                break

            s = set(
                filter(
                    lambda x: x in normal_points or x in toggled_points,
                    i.AABB.generate_bounded_points(),
                )
            )

            if i.operation == _Operation.TURN_OFF:
                normal_points.difference_update(s)

                # We turn them off, so the toggle turns ultimately turns them back on
                start_sz_toggled = len(toggled_points)
                toggled_points.difference_update(s)
                number_on += start_sz_toggled - len(toggled_points)
            elif i.operation == _Operation.TURN_ON:
                start_sz_normal = len(normal_points)
                normal_points.difference_update(s)
                number_on += start_sz_normal - len(normal_points)

                # We turn them on, then the toggle turns ultimately turns them off
                toggled_points.difference_update(s)
            elif i.operation == _Operation.TOGGLE:
                total = len(toggled_points) + len(normal_points)
                tp_back_to_normal = toggled_points.intersection(s)
                toggled_points.symmetric_difference_update(
                    s.intersection(normal_points)
                )
                normal_points.update(tp_back_to_normal.intersection(s))
                print(total, len(toggled_points) + len(normal_points))
                assert len(toggled_points) + len(normal_points) == total
            else:
                raise NotImplementedError(i.operation)

        number_on += len(toggled_points)

        return number_on

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
