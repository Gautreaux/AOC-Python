from .point import Point2
from typing import Any, Iterator
from typing import Callable


class Grid2d:
    """Two Dimensional Grid"""

    def __init__(self, rows: list[list[Any]]):
        self.rows: list[list[Any]] = rows

        # Assert all rows are the same length
        assert len({len(r) for r in rows}) == 1
        assert rows  # is not empty
        assert rows[0]  # is not empty

    def new_map_same_dimensions(self, default_value=None) -> "Grid2d":
        """Create a new map with the same dimensions"""
        x, y = self.dimensions
        new_row = [default_value] * x
        return Grid2d([new_row] * y)

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

    def at(self, point: Point2 | tuple[int, int]) -> str:
        """Get the entry at the point"""
        if point[0] < 0:
            raise IndexError()
        if point[1] < 0:
            raise IndexError()
        return self.rows[point[1]][point[0]]

    def iter_cells(self) -> Iterator[tuple[Point2, Any]]:
        """Iterate the cells of this grid"""
        for y, row in enumerate(self.rows):
            for x, e in enumerate(row):
                yield (Point2(x, y), e)

    def generate_matching_points(self, value: Any) -> Iterator[tuple[Point2, Any]]:
        """Generate the matching points"""
        for p, v in self.iter_cells():
            if v == value:
                yield (p, v)

    def generate_neighbor_points(
        self,
        point: Point2,
        include_diagonals: bool = False,
        value_filter: Callable[[Any], bool] = lambda _: True,
    ) -> Iterator[tuple[Point2, Any]]:
        """Generate the neighbor points of the given point"""

        assert isinstance(point, Point2)

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
