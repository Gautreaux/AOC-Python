from dataclasses import dataclass, field
from typing import Iterator, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.PointTransforms import Direction2
from AOC_Lib.Grid2d import Grid2d, Point2


@dataclass
class RegionSideSegment:
    """A segment of a side around a region"""

    # A point inside the region
    point: Point2

    # The direction from the point to the outside of the region
    direction: Direction2

    def __hash__(self) -> int:
        return hash((self.point, self.direction))


@dataclass
class Region:
    """A region of the same crops"""

    crop: str
    points: set[Point2] = field(default_factory=set)

    def __str__(self) -> str:
        return f"Region<{self.crop}, {len(self.points)}>"

    def get_cost(self) -> int:
        """Get the cost of this region"""
        return self.get_area() * self.get_perimeter_len()

    def get_bulk_cost(self) -> int:
        """Get the bulk cost of this region"""
        return self.get_area() * self.get_sides_count()

    def get_area(self) -> int:
        """Return the area of this region"""
        return len(self.points)

    @staticmethod
    def _generate_all_neighbors(point: Point2) -> Iterator[tuple[Point2, Direction2]]:
        """Generate all neighbors of a point"""
        for direction in Direction2:
            # Needed because direction.get_transform is a DiscretePoint2
            # This needs to be fixed (evenutally)
            t = direction.get_transform
            neighbor = point + Point2(t[0], t[1])
            yield neighbor, direction

    def generate_side_segements(self) -> Iterator[RegionSideSegment]:
        """Generate the side segements for this region"""
        for point in self.points:
            for neighbor, direction in self._generate_all_neighbors(point):
                if neighbor not in self.points:
                    yield RegionSideSegment(point, direction)

    def get_perimeter_len(self) -> int:
        """Get the length of the perimeter of this region"""
        return sum(1 for _ in self.generate_side_segements())

    def get_sides_count(self) -> int:
        """Get a count of the number of distinct sides in this region"""
        side_segments = set(self.generate_side_segements())

        count_sides: int = 0

        # Reduce the side segments down to the actual sides
        while side_segments:
            count_sides += 1

            this_side_all_segments: set[RegionSideSegment] = set()
            frontier: list[RegionSideSegment] = []

            frontier.append(next(iter(side_segments)))

            while frontier:
                current_segment = frontier.pop()
                this_side_all_segments.add(current_segment)

                for neighbor, _ in self._generate_all_neighbors(current_segment.point):
                    ns = RegionSideSegment(neighbor, current_segment.direction)
                    if (ns in side_segments) and (ns not in this_side_all_segments):
                        frontier.append(ns)

            side_segments -= this_side_all_segments
        return count_sides


class Solution_2024_12(SolutionBase):
    """https://adventofcode.com/2024/day/12"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.region_map: Grid2d = Grid2d([list(c) for c in self.input_str_list()])
        self.regions: list[Region] = []

        point_to_region: dict[Point2, Region] = {}

        # Build the list of regions
        for point, crop in self.region_map.iter_cells():
            if point in point_to_region:
                continue

            this_region_points = set(
                self.region_map.generate_flood_fill_matching_points(point)
            )
            this_region = Region(crop, this_region_points)
            self.regions.append(this_region)
            for p in this_region_points:
                point_to_region[p] = this_region

        print(f"Done building {len(self.regions)} regions")

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(region.get_cost() for region in self.regions)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return sum(region.get_bulk_cost() for region in self.regions)
