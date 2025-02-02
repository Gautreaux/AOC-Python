from enum import Enum
from typing import Iterator, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.PointTransforms import Direction2
from AOC_Lib.Grid2d import Grid2d, Point2


class PipeComponent(Enum):
    """Component for the Pipes"""

    VERTICAL_PIPE = "|"
    HORIZONTAL_PIPE = "-"
    SOUTH_WEST_CORNER = "L"
    NORTH_WEST_CORNER = "F"
    NORTH_EAST_CORNER = "7"
    SOUTH_EAST_CORNER = "J"
    GROUND = "."
    START = "S"

    @staticmethod
    def find_by_inbound_connections(
        connections: tuple[Direction2, Direction2]
    ) -> "PipeComponent":
        """Find the PipeComponent that has the given inbound connections"""
        connections_set = set(connections)
        for candidate in PipeComponent:
            if candidate == PipeComponent.GROUND:
                continue
            if set(candidate.inbound_connections) == connections_set:
                return candidate
        raise ValueError(
            f"Could not find PipeComponent for inbound connections {connections}"
        )

    @staticmethod
    def find_by_outbound_connections(
        connections: tuple[Direction2, Direction2]
    ) -> "PipeComponent":
        """Find the PipeComponent that has the given outbound connections"""
        connections_set = set(connections)
        for candidate in PipeComponent:
            if candidate == PipeComponent.GROUND:
                continue
            if set(candidate.outbound_connections) == connections_set:
                return candidate
        raise ValueError(
            f"Could not find PipeComponent for outbound connections {connections}"
        )

    @property
    def inbound_connections(self) -> tuple[Direction2, Direction2]:
        """Which directions from which we can enter this pipe

        This is the format of position.direction -> this pipe
        I.e. what transforms can be applied from other pipes to connect to this pipe successfully
        """
        if self == PipeComponent.VERTICAL_PIPE:
            return (Direction2.UP, Direction2.DOWN)
        if self == PipeComponent.HORIZONTAL_PIPE:
            return (Direction2.LEFT, Direction2.RIGHT)
        if self == PipeComponent.NORTH_WEST_CORNER:
            return (Direction2.UP, Direction2.LEFT)
        if self == PipeComponent.NORTH_EAST_CORNER:
            return (Direction2.UP, Direction2.RIGHT)
        if self == PipeComponent.SOUTH_WEST_CORNER:
            return (Direction2.DOWN, Direction2.LEFT)
        if self == PipeComponent.SOUTH_EAST_CORNER:
            return (Direction2.DOWN, Direction2.RIGHT)
        if self == PipeComponent.GROUND:
            raise RuntimeError("Ground pipes do not have an inbound connection")
        if self == PipeComponent.START:
            raise RuntimeError("Start pipes do not have an inbound connection")
        raise RuntimeError(f"Invalid Pipe Component: {self}")

    @property
    def outbound_connections(self) -> tuple[Direction2, Direction2]:
        """Which directions from which we can enter this pipe

        This is the format of position.direction -> this pipe
        I.e. what transforms can be applied from other pipes to connect to this pipe successfully
        """
        if self == PipeComponent.GROUND:
            raise RuntimeError("Ground pipes do not have an outbound connection")
        if self == PipeComponent.START:
            raise RuntimeError("Start pipes do not have an outbound connection")

        ic = self.inbound_connections
        return (ic[0].opposite, ic[1].opposite)


class InsideOutsideStatus(Enum):
    """Represent if the tile is inside or outside the start loop"""

    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    ON = "ON"
    UNASSIGNED = "UNASSIGNED"


class Solution_2023_10(SolutionBase):
    """https://adventofcode.com/2023/day/10"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        rows = [[PipeComponent(c) for c in line] for line in self.input_str_list()]

        self.map: Grid2d[PipeComponent] = Grid2d(rows)

        start_pos = list(self.map.generate_matching_points(PipeComponent.START))
        if not start_pos:
            raise RuntimeError("No Starting position found!")
        if len(start_pos) > 1:
            raise RuntimeError("Multiple starting positions found")

        self.start_pos: Point2 = start_pos[0][0]

        start_pipe = self._determine_start_poisition_pipe()
        print(f"Determined start pipe to be a {start_pipe}")
        self.map.update(self.start_pos, start_pipe)

    def _determine_start_poisition_pipe(self) -> PipeComponent:
        """Determine what type of pipe is at the start position"""
        connected_neighbors: list[Direction2] = []

        for direction in Direction2:
            # Hack to convert DiscretePoint2 to Point2
            # Notice we also flip y so that "up" is negative y
            neighbor_pos = self.start_pos + Point2(
                direction.get_transform.x, -direction.get_transform.y
            )

            try:
                neighbor_pipe = self.map.at(neighbor_pos)
            except IndexError:
                # Outside the map; No need to check
                continue

            if neighbor_pipe == PipeComponent.GROUND:
                continue

            if direction in neighbor_pipe.inbound_connections:
                connected_neighbors.append(direction)

        if len(connected_neighbors) < 2:
            raise RuntimeError("Start tile is only connected by one pipe")
        if len(connected_neighbors) > 2:
            raise RuntimeError("Start tile is connected by more than two pipes")

        return PipeComponent.find_by_outbound_connections(connected_neighbors)  # type: ignore

    def _determine_next_dir_and_pos(
        self, current_pos: Point2, prior_pos: Point2 | None
    ) -> tuple[Direction2, Point2]:
        """Determine the next dir from the current pos and the prior pos"""
        current_pipe = self.map.at(current_pos)
        if prior_pos is None:
            # this is the first; Pick any direction (but check its not a start / ground)
            for candidate in current_pipe.outbound_connections:
                candidate_pos = current_pos + Point2(
                    candidate.get_transform.x, -candidate.get_transform.y
                )
                candidate_pipe = self.map.at(candidate_pos)
                if candidate_pipe not in [PipeComponent.START, PipeComponent.GROUND]:
                    return candidate, candidate_pos
            raise RuntimeError(
                f"All pipes connected to {current_pipe} are ground or start"
            )

        for candidate in current_pipe.outbound_connections:
            candidate_pos = current_pos + Point2(
                candidate.get_transform.x, -candidate.get_transform.y
            )
            if candidate_pos != prior_pos:
                return candidate, candidate_pos

        # Should not be able to get here
        raise RuntimeError(
            f"[EXPECT UNREACHABLE] No valid direction from {current_pipe} with prior {prior_pos}"
        )

    def _walk_pipe(self, start_pos: Point2) -> Iterator[tuple[Point2, PipeComponent]]:
        """Walk the pipe from the start position, yielding each point as we go"""
        prior_pos: Point2 | None = None
        current_pos: Point2 = start_pos

        yield (current_pos, self.map.at(current_pos))

        while True:
            _, next_pos = self._determine_next_dir_and_pos(current_pos, prior_pos)
            next_pipe = self.map.at(next_pos)

            if next_pipe == PipeComponent.START:
                raise RuntimeError("Found unexpected start pipe!")
            if next_pipe == PipeComponent.GROUND:
                # Pipe is broken, no further to walk
                return

            yield (next_pos, next_pipe)

            prior_pos = current_pos
            current_pos = next_pos

    def _get_start_loop(self) -> list[Point2]:
        """Returns loop formed with the start positions"""
        seen_pos: set[Point2] = set()
        pipe_walk: list[Point2] = []

        for pos, _ in self._walk_pipe(self.start_pos):
            if pos in seen_pos:
                break
            seen_pos.add(pos)
            pipe_walk.append(pos)
        return pipe_walk

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        start_loop = self._get_start_loop()

        print("Start loop size is: ", len(start_loop))

        return len(start_loop) // 2

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        positions_on_start_loop = set(self._get_start_loop())

        inside_outside_grid: Grid2d[InsideOutsideStatus] = (
            self.map.new_map_same_dimensions_factory(
                lambda: InsideOutsideStatus.UNASSIGNED
            )
        )

        def flood_fill_inside_outside_marker(start_at: Point2):
            nonlocal inside_outside_grid
            frontier: list[Point2] = [start_at]

            value = inside_outside_grid.at(start_at)

            if value not in [InsideOutsideStatus.INSIDE, InsideOutsideStatus.OUTSIDE]:
                raise ValueError(f"Invalid value {value} at {start_at}")

            while frontier:
                current = frontier.pop()
                inside_outside_grid.update(current, value)

                for n, v in inside_outside_grid.generate_neighbor_points(current):
                    if v == InsideOutsideStatus.UNASSIGNED:
                        inside_outside_grid.update(n, value)
                        frontier.append(n)

        for p in positions_on_start_loop:
            inside_outside_grid.update(p, InsideOutsideStatus.ON)

        for p, v in inside_outside_grid.iter_edges():
            if v == InsideOutsideStatus.UNASSIGNED:
                inside_outside_grid.update(p, InsideOutsideStatus.OUTSIDE)

        for e in [
            p
            for p, _ in inside_outside_grid.generate_matching_points(
                InsideOutsideStatus.OUTSIDE
            )
        ]:
            flood_fill_inside_outside_marker(e)

        from collections import Counter

        c = Counter(v for _, v in inside_outside_grid.iter_cells())
        print(c)

        # Need to finish computing the crossing value
        #   Once again, a dual graph would be helpful
        # Some thoughts: Looking for patterns
        #   O|X --> X is Inside
        #   I|X --> X is Outside
        #   O||X --> X is Outside
        #   I||X --> X is Inside
        #
        #   I
        #   -   --> X is Outside
        #   X
        #
        #   O
        #   -   --> X is Inside
        #   X
        #
        #   I
        #   -   --> X is Inside
        #   -
        #   X
        #
        #   O
        #   -   --> X is Outside
        #   -
        #   X
        #
        #   F-7
        #   |X|
        #   LFJ
        #   ||  --> X is Y
        #  -JL-
        #  |YY|
        #
        # Need 2 things:
        #   1. some concept of regions and if a region is inside or outside (union find)
        #   2. a function: determine_crossings_count(point, region)
        #       if crossing count is even, then same inside/outside
        #       else the opposite inside/outside

        raise NotImplementedError()
