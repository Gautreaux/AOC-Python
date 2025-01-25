from dataclasses import dataclass, field
from functools import cache
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2

# Why solve efficiently, when you can solve enough and cache
#   After all the rewrites, ended up pretty efficient anyway


@cache
def get_tail_pos_head_relative(tail: DiscretePoint2) -> DiscretePoint2:
    """Return the new position of the tail in the head centered coordinate system"""

    # They are on top of each other
    if tail == DiscretePoint2(0, 0):
        return DiscretePoint2(0, 0)

    # They are next to eachother on axis (no change)
    if abs(tail.x) + abs(tail.y) == 1:
        return tail

    # They are next to eachother diagonally (no change)
    if tail.x in [1, -1] and tail.y in [1, -1]:
        return tail

    # Special Part 2 case: double diagonal
    if tail.x in [-2, 2] and tail.y in [-2, 2]:
        return DiscretePoint2(tail.x // 2, tail.y // 2)

    # Check column
    if tail.y == 2:
        return DiscretePoint2(0, 1)
    if tail.y == -2:
        return DiscretePoint2(0, -1)

    # Check Row
    if tail.x == 2:
        return DiscretePoint2(1, 0)
    if tail.x == -2:
        return DiscretePoint2(-1, 0)

    raise RuntimeError()


@dataclass
class PlanckRope:

    head: DiscretePoint2 = DiscretePoint2(0, 0)
    tail: DiscretePoint2 = DiscretePoint2(0, 0)

    def step_once(self, direction):
        """Apply one step"""
        adj = {
            "R": DiscretePoint2(1, 0),
            "U": DiscretePoint2(0, 1),
            "D": DiscretePoint2(0, -1),
            "L": DiscretePoint2(-1, 0),
        }[direction]

        self.head: DiscretePoint2 = self.head + adj
        self.update_tail()

    def snap_head(self, pos: DiscretePoint2):
        """Snap the head to the position and then update the tail"""
        self.head = pos
        self.update_tail()

    def update_tail(self):
        local = self.tail - self.head
        adjusted = get_tail_pos_head_relative(local)
        self.tail = self.head + adjusted


class MultiRope:
    """Multiple, chained Planck Rope"""

    def __init__(self, length: int) -> None:
        self.segments: list[PlanckRope] = []

        while len(self.segments) < length:
            self.segments.append(PlanckRope())

    @property
    def head(self) -> DiscretePoint2:
        return self.segments[0].head

    @property
    def tail(self) -> DiscretePoint2:
        return self.segments[-1].tail

    def step_once(self, direction):
        """Apply one step to the head, and propagate changes through the chain"""
        self.segments[0].step_once(direction)
        for i in range(1, len(self.segments)):
            self.segments[i].snap_head(self.segments[i - 1].tail)


class Solution_2022_09(SolutionBase):
    """https://adventofcode.com/2022/day/9"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        rope = PlanckRope()
        all_t_pos = set()

        for line in self.input_str_list(include_empty_lines=False):
            direction, amount = line.split(" ")

            for _ in range(int(amount)):
                try:
                    # self.step_once(direction)
                    rope.step_once(direction)
                except:
                    print(rope)
                    raise

                # all_t_pos.add(self.t_pos)
                all_t_pos.add(rope.tail)

        return len(all_t_pos)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        rope = MultiRope(9)
        all_t_pos = set()

        for line in self.input_str_list(include_empty_lines=False):
            direction, amount = line.split(" ")

            for _ in range(int(amount)):
                try:
                    # self.step_once(direction)
                    rope.step_once(direction)
                except:
                    print(rope)
                    raise

                # all_t_pos.add(self.t_pos)
                all_t_pos.add(rope.tail)
        print(rope.segments)
        return len(all_t_pos)
