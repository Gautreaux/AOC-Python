from .point import Point2
from typing import Callable, TypeVar, Generic, Iterator, Self

T = TypeVar("T")
Z = TypeVar("Z")


class Grid2d(Generic[T]):
    """Two Dimensional Grid"""

    def __init__(self, rows: list[list[T]]):
        self.rows: list[list[T]] = rows

        # Assert all rows are the same length
        assert len({len(r) for r in rows}) == 1
        assert rows  # is not empty
        assert rows[0]  # is not empty

    def new_map_same_dimensions(
        self,
        default_value: Z = None,
    ) -> "Grid2d[Z]":
        """Create a new map with the same dimensions"""
        x, y = self.dimensions
        new_row = [default_value] * x
        return Grid2d([new_row] * y)

    def new_map_same_dimensions_factory(
        self, default_value_factory: Callable[[], Z]
    ) -> "Grid2d[Z]":
        """Create a new map with the same dimensions"""
        rows = [
            [default_value_factory() for _ in range(self.width)]
            for _ in range(self.height)
        ]
        return Grid2d(rows)

    @staticmethod
    def from_list_str(lines: list[str]) -> "Grid2d[str]":
        """Create a new Grid2d from a list of strings"""
        rows = [list(line) for line in lines]
        return Grid2d(rows)

    def __str__(self) -> str:
        x, y = self.dimensions
        return f"{self.__class__.__name__}<{x, y}>"

    def full_str(self) -> str:
        """Return a fill string representation"""
        return "\n".join(["".join(map(str, r)) for r in self.rows])

    @property
    def dimensions(self) -> tuple[int, int]:
        """Return dimensions as an x,y tuple"""
        return (len(self.rows[0]), len(self.rows))

    @property
    def width(self) -> int:
        """Return the width (x-dimension) of this grid"""
        return self.dimensions[1]

    @property
    def height(self) -> int:
        """Return the width (y-dimension) of this grid"""
        return self.dimensions[0]

    def is_valid_point(self, point: Point2 | tuple[int, int]):
        """Return True iif this is a valid point in the grid"""
        if point[0] < 0:
            return False
        if point[1] < 0:
            return False
        if point[0] >= self.width:
            return False
        if point[1] >= self.height:
            return False
        return True

    def update(self, point: Point2 | tuple[int, int], value: T) -> Self:
        """Update the value at the given point"""
        if not self.is_valid_point(point):
            raise IndexError(point)
        self.rows[point[1]][point[0]] = value
        return self

    def at(self, point: Point2 | tuple[int, int]) -> T:
        """Get the entry at the point"""
        if not self.is_valid_point(point):
            raise IndexError(point)
        return self.rows[point[1]][point[0]]

    def iter_cells(self) -> Iterator[tuple[Point2, T]]:
        """Iterate the cells of this grid"""
        for y, row in enumerate(self.rows):
            for x, e in enumerate(row):
                yield (Point2(x, y), e)

    def iter_edges(self) -> Iterator[tuple[Point2, T]]:
        """Iterate the cells along the edge of the grid"""

        # Generate the top row
        for x in range(self.width):
            p = Point2(x, 0)
            yield (p, self.at(p))

        if self.height == 1:
            return

        if self.width == 1:
            return

        for y in range(1, self.height - 1):
            p = Point2(self.width - 1, y)
            yield (p, self.at(p))

        for x in reversed(range(self.width)):
            p = Point2(x, self.height - 1)
            yield (p, self.at(p))

        for y in reversed(range(1, self.height - 1)):
            p = Point2(0, y)
            yield (p, self.at(p))

    def generate_matching_points(self, value: T) -> Iterator[tuple[Point2, T]]:
        """Generate the matching points"""
        for p, v in self.iter_cells():
            if v == value:
                yield (p, v)

    def generate_flood_fill_matching_points(self, start: Point2) -> Iterator[Point2]:
        """Generate all the points touching start that have the same value as start (including start)"""
        if not self.is_valid_point(start):
            raise IndexError(start)

        v = self.at(start)

        yield start

        seen: set[Point2] = set()
        frontier: list[Point2] = []

        frontier.append(start)

        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            yield current
            seen.add(current)

            frontier.extend(
                p
                for p, _ in self.generate_neighbor_points(
                    current, value_filter=lambda x: x == v
                )
            )

    def generate_neighbor_points(
        self,
        point: Point2,
        include_diagonals: bool = False,
        value_filter: Callable[[T], bool] = lambda _: True,
    ) -> Iterator[tuple[Point2, T]]:
        """Generate the neighbor points of the given point"""

        if not self.is_valid_point(point):
            raise IndexError(point)

        transforms_xy = (
            Point2(1, 0),
            Point2(0, 1),
            Point2(
                -1,
                0,
            ),
            Point2(0, -1),
        )

        transforms_xy_diagonals = (
            Point2(1, 0),
            Point2(1, 1),
            Point2(0, 1),
            Point2(-1, 1),
            Point2(-1, 0),
            Point2(-1, -1),
            Point2(0, -1),
            Point2(1, -1),
        )

        transforms = transforms_xy_diagonals if include_diagonals else transforms_xy

        for t in transforms:
            new_p = point + t
            try:
                value = self.at(new_p)
            except IndexError:
                pass
            else:
                if value_filter(value):
                    yield (new_p, value)
