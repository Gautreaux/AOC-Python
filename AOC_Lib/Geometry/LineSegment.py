from dataclasses import dataclass
from typing import Iterator, Optional

from .Point import DiscretePoint2


class DegenerateMultipoint(Exception):
    """Raised when a multipoint-solution is discovered (generally on intersections)"""


@dataclass(frozen=True)
class Segment2_DiscreteAA:
    """An Axis-Aligned (horizontal or vertical) segment in discrete 2D space"""

    start_pos: DiscretePoint2
    end_pos: DiscretePoint2

    def __post_init__(self):
        if not (self.is_vertical or self.is_horizontal):
            raise RuntimeError("Segment is not Axis Aligned")

    def __len__(self):
        return self.start_pos.manhattan_distance(self.end_pos)

    @property
    def is_vertical(self) -> bool:
        """Return `True` iff this a vertical segment"""
        return self.start_pos.x == self.end_pos.x

    @property
    def is_horizontal(self) -> bool:
        """Return `True` iff this is a horizontal segment"""
        return self.start_pos.y == self.end_pos.y

    @property
    def is_degenerate(self) -> bool:
        """Return `True` iff this segment is degenerate"""
        return self.start_pos == self.end_pos

    @property
    def min_x(self):
        return min(self.start_pos.x, self.end_pos.x)

    @property
    def max_x(self):
        return max(self.start_pos.x, self.end_pos.x)

    @property
    def min_y(self):
        return min(self.start_pos.y, self.end_pos.y)

    @property
    def max_y(self):
        return max(self.start_pos.y, self.end_pos.y)

    def _get_intersection_vertical(
        self, other: "Segment2_DiscreteAA"
    ) -> Optional["Segment2_DiscreteAA"]:
        """Worker for when both segments are vertical"""

        if self.start_pos.x != other.start_pos.x:
            return None
        elif self.min_y > other.max_y:
            return None
        elif other.min_y > self.max_y:
            return None
        elif self.min_y == other.max_y:
            return DiscretePoint2(self.start_pos.x, self.min_y)
        elif self.max_y == other.min_y:
            return DiscretePoint2(self.start_pos.x, self.max_y)
        else:
            raise DegenerateMultipoint()

    def _get_intersection_horizontal(
        self, other: "Segment2_DiscreteAA"
    ) -> Optional["Segment2_DiscreteAA"]:
        """Worker for when both segments are horizontal"""

        if self.start_pos.y != other.start_pos.y:
            return None
        elif self.min_x > other.max_x:
            return None
        elif other.min_x > self.max_x:
            return None
        elif self.min_x == other.max_x:
            return DiscretePoint2(self.min_x, self.start_pos.y)
        elif self.max_x == other.min_x:
            return DiscretePoint2(self.max_x, self.start_pos.y)
        else:
            raise DegenerateMultipoint()

    def get_intersection(
        self, other: "Segment2_DiscreteAA"
    ) -> Optional[DiscretePoint2]:
        """Get the intersection point of this segment with other"""
        if self.is_vertical and other.is_vertical:
            return self._get_intersection_vertical(other)
        elif self.is_horizontal and other.is_horizontal:
            return self._get_intersection_horizontal(other)

        vertical_segment = self if self.is_vertical else other
        horizontal_segment = self if self.is_horizontal else other

        if vertical_segment.start_pos.x < horizontal_segment.min_x:
            return None
        elif vertical_segment.start_pos.x > horizontal_segment.max_x:
            return None
        elif horizontal_segment.start_pos.y < vertical_segment.min_y:
            return None
        elif horizontal_segment.start_pos.y > vertical_segment.max_y:
            return None

        return DiscretePoint2(
            vertical_segment.start_pos.x, horizontal_segment.start_pos.y
        )

    def is_point_on_segment(self, point: DiscretePoint2) -> bool:
        """Return `True` iff point is on segment"""
        if self.is_vertical:
            return (
                point.x == self.start_pos.x
                and point.y >= self.min_y
                and point.y <= self.max_y
            )
        else:
            return (
                point.y == self.start_pos.y
                and point.x >= self.min_x
                and point.x <= self.max_x
            )

    def iter_points(self) -> Iterator[DiscretePoint2]:
        """Iterate from the start to the end point, inclusive"""

        if self.start_pos == self.end_pos:
            yield self.start_pos
            return

        m = self.end_pos - self.start_pos

        modifier = DiscretePoint2(
            0 if m.x == 0 else (1 if m.x > 0 else -1),
            0 if m.y == 0 else (1 if m.y > 0 else -1),
        )

        t = self.start_pos

        while t != self.end_pos:
            yield t
            t += modifier
        yield self.end_pos
