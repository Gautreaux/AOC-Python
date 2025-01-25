from dataclasses import dataclass
import itertools
from typing import Optional


from AOC_Lib.Geometry.LineSegment import Segment2_DiscreteAA, DegenerateMultipoint
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass(frozen=True)
class Wire:

    segments: tuple[Segment2_DiscreteAA]

    @classmethod
    def from_operations(
        cls, operations: list[str], start_pos: DiscretePoint2 = DiscretePoint2(0, 0)
    ) -> "Wire":
        """Build a Wire for a list of operations"""

        segments: list[Segment2_DiscreteAA] = []

        last_pos = start_pos

        for op in operations:
            instr = op[0]
            amount = int(op[1:])

            end_pos = {
                "R": (lambda s, a: DiscretePoint2(s.x + a, s.y)),
                "L": (lambda s, a: DiscretePoint2(s.x - a, s.y)),
                "U": (lambda s, a: DiscretePoint2(s.x, s.y + a)),
                "D": (lambda s, a: DiscretePoint2(s.x, s.y - a)),
            }[instr](last_pos, amount)

            segments.append(Segment2_DiscreteAA(last_pos, end_pos))
            last_pos = end_pos
        return cls(tuple(segments))

    def get_intersection_points(self, other: "Wire") -> list[DiscretePoint2]:
        """Get all the point where the wires intersect"""

        to_return = []

        for segment_a, segment_b in itertools.product(self.segments, other.segments):
            try:
                p = segment_a.get_intersection(segment_b)
            except DegenerateMultipoint:
                print("WARNING degenerate multipoint found")
                continue
            if p:
                to_return.append(p)
        return to_return

    def get_point_depth_on_wire(self, point: DiscretePoint2) -> int:
        """Return how far along wire `point` is
        Raise an error if point is not on wire
        """
        counter = 0
        for s in self.segments:
            if s.is_point_on_segment(point):
                return counter + point.manhattan_distance(s.start_pos)
            else:
                counter += len(s)
        raise RuntimeError()


class Solution_2019_03(SolutionBase):
    """https://adventofcode.com/2019/day/3"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.wires: list[Wire] = []

        for line in self.input_str_list(include_empty_lines=False):
            self.wires.append(Wire.from_operations(line.split(",")))

        assert len(self.wires) == 2

        self.intersections = self.wires[0].get_intersection_points(self.wires[1])

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        origin = DiscretePoint2(0, 0)

        return min(
            map(
                lambda x: x.manhattan_distance(origin),
                filter(
                    lambda p: not p.is_origin,
                    self.intersections,
                ),
            )
        )

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        wire_a, wire_b = self.wires

        return min(
            map(
                lambda x: wire_a.get_point_depth_on_wire(x)
                + wire_b.get_point_depth_on_wire(x),
                filter(
                    lambda p: not p.is_origin,
                    self.intersections,
                ),
            )
        )
