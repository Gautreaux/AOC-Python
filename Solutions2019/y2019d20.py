# from AOC_Lib.name import *

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional
from dataclasses import dataclass


from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T


_DEGENERATE_POINT = DiscretePoint2(-1, -1)


@dataclass(frozen=True)
class PortalConnection:
    label: str
    inside_pos: DiscretePoint2
    outside_pos: DiscretePoint2

    @property
    def is_single_connection(self) -> bool:
        """Return `True` iff this is a single connection
        i.e. at the start and end points
        """
        return (
            self.inside_pos == _DEGENERATE_POINT
            and self.outside_pos != _DEGENERATE_POINT
        ) or (
            self.outside_pos == _DEGENERATE_POINT
            and self.inside_pos != _DEGENERATE_POINT
        )

    @property
    def get_single_connection(self) -> DiscretePoint2:
        """Get the singular point in cases of a single connection
        i.e. at the start and end points
        """
        assert self.is_single_connection
        return (
            self.inside_pos
            if self.outside_pos == _DEGENERATE_POINT
            else self.outside_pos
        )


@unique
class TileType(IntEnum):
    """The types of tiles"""

    PASSAGE = (0,)
    WALL = (1,)
    PORTAL = (2,)
    WHITESPACE = (3,)

    def render(self) -> str:
        if self.value == TileType.PASSAGE:
            return "."
        elif self.value == TileType.WALL:
            return "#"
        elif self.value == TileType.PORTAL:
            return "P"
        elif self.value == TileType.WHITESPACE:
            return " "
        raise NotImplementedError(self)


class DonutMaze:

    def __init__(
        self, maze: list[list[TileType]], portal_labels: dict[str, PortalConnection]
    ) -> None:
        self._maze: list[list[TileType]] = maze
        self._labels_to_portals: dict[str, PortalConnection] = portal_labels
        self._positions_to_portals: dict[DiscretePoint2, PortalConnection] = (
            self._getPositionsToPortals()
        )

    @classmethod
    def fromLines(cls, lineList: list[str]) -> "DonutMaze":
        """Build an return an object from the line list"""
        # assert that the maze "starts at 2,2"
        assert lineList[0][0] == " "
        assert lineList[1][0] == " "
        assert lineList[0][1] == " "
        assert lineList[1][1] == " "
        assert lineList[0][2] == " "
        assert lineList[1][2] == " "
        assert lineList[2][0] == " "
        assert lineList[2][1] == " "
        assert lineList[2][2] == "#"

        my_maze: list[list[TileType]] = []
        raw_portal_labels: dict[tuple[int, int], str] = {}

        # parse the input and find walls, passages, tiles, etc
        for y_value, row in enumerate(lineList):
            maze_row: list[TileType] = []
            for x_value, char in enumerate(row):
                if char == ".":
                    maze_row.append(TileType.PASSAGE)
                elif char == "#":
                    maze_row.append(TileType.WALL)
                elif char == " ":
                    maze_row.append(TileType.WHITESPACE)
                elif char == "\n":
                    break
                elif char == "\r":
                    break
                elif (ord(char) >= ord("A")) and (ord(char) <= ord("Z")):
                    raw_portal_labels[(x_value, y_value)] = char
                    maze_row.append(TileType.WHITESPACE)
                else:
                    raise RuntimeError(f"Unrecognized character: {char}")
            my_maze.append(maze_row)

        # local helper function
        def getPassagePosition(x_1, y_1, x_2, y_2) -> DiscretePoint2:
            """get the passage position from the two letter positions
            For the two positions of the letters,
                return the position of the adjacent PASSAGE
            """
            if y_1 == y_2:
                # horizontal case
                candidate_x_1 = min(x_1, x_2) - 1
                candidate_x_2 = max(x_1, x_2) + 1  # candidate_1 + 2?
                candidate_y_1 = y_1
                candidate_y_2 = y_1
            else:
                # vertical case
                candidate_x_1 = x_1
                candidate_x_2 = x_1
                candidate_y_1 = min(y_1, y_2) - 1
                candidate_y_2 = max(y_1, y_2) + 1

            for x, y in [
                (candidate_x_1, candidate_y_1),
                (candidate_x_2, candidate_y_2),
            ]:
                try:
                    if x < 0 or y < 0:
                        continue
                    # print(f"Checking {x},{y} -> ", my_maze[y][x])
                    if my_maze[y][x] == TileType.PASSAGE:
                        return DiscretePoint2(x, y)
                except IndexError:
                    pass
            raise RuntimeError("No neighboring position was a passage")

        # mapping of portal label to position
        portals_to_positions: defaultdict[str, list[DiscretePoint2]] = defaultdict(list)

        # Build all the portals:
        # For each letter label:
        #   try and find the matching label (to get the two-letter portal name)
        #   find the position of the passage this corresponds to
        while raw_portal_labels:
            (this_x, this_y), this_letter = next(iter(raw_portal_labels.items()))

            num_matches = 0

            for other_x, other_y, raw_p_name in [
                (this_x + 1, this_y, "{this_letter}{other_letter}"),
                (this_x - 1, this_y, "{other_letter}{this_letter}"),
                (this_x, this_y + 1, "{this_letter}{other_letter}"),
                (this_x, this_y - 1, "{other_letter}{this_letter}"),
            ]:
                try:
                    other_letter = raw_portal_labels[(other_x, other_y)]
                except KeyError:
                    continue

                portal_name = raw_p_name.format(
                    this_letter=this_letter,
                    other_letter=other_letter,
                )

                portal_pos = getPassagePosition(this_x, this_y, other_x, other_y)
                portals_to_positions[portal_name].append(portal_pos)
                num_matches += 1
                my_maze[portal_pos[1]][portal_pos[0]] = TileType.PORTAL
                raw_portal_labels.pop((this_x, this_y))
                raw_portal_labels.pop((other_x, other_y))
            if num_matches == 0:
                raise RuntimeError(
                    f"This {(this_x, this_y)} does not have another candidate nearby"
                )
            if num_matches > 1:
                raise RuntimeError(
                    f"This {(this_x, this_y)} has multiple candidate nearby"
                )

        # check that all the portals have exactly two candidates in their named pair
        #   except for the start and end, which do not
        for k, v in portals_to_positions.items():
            if k in ["ZZ", "AA"]:
                assert len(v) == 1
                continue
            if len(v) != 2:
                print(f"Key {k} got only one portal {v}. Two expected.")
            assert len(v) == 2

        paired_portals: dict[str, PortalConnection] = {}

        for label, positions in portals_to_positions.items():
            first_pos = positions[0]
            first_pos_is_outside = False

            does_x_imply_outside = first_pos[0] < 4 or (first_pos[0] + 4) >= len(
                my_maze[0]
            )
            does_y_imply_outside = first_pos[1] < 4 or (first_pos[1] + 4) >= len(
                my_maze
            )

            first_pos_is_outside = does_x_imply_outside or does_y_imply_outside

            if len(positions) == 1:
                assert label in ["AA", "ZZ"]
                assert first_pos_is_outside
                positions.append(_DEGENERATE_POINT)
            else:
                assert len(positions) == 2

            paired_portals[label] = PortalConnection(
                label=label,
                inside_pos=(positions[1] if first_pos_is_outside else positions[0]),
                outside_pos=(positions[0] if first_pos_is_outside else positions[1]),
            )

        return cls(my_maze, paired_portals)

    def _getPositionsToPortals(self) -> dict[DiscretePoint2, PortalConnection]:
        """Use the portal labels to positions map to get a positions to portal connection map"""
        to_return = {}
        for portal_connection in self._labels_to_portals.values():
            if portal_connection.is_single_connection:
                p = portal_connection.get_single_connection
                assert p not in to_return
                to_return[p] = portal_connection
            else:
                assert portal_connection.inside_pos not in to_return
                to_return[portal_connection.inside_pos] = portal_connection
                assert portal_connection.outside_pos not in to_return
                to_return[portal_connection.outside_pos] = portal_connection
        return to_return

    @property
    def start_pos(self) -> DiscretePoint2:
        """The position for label `AA`"""
        return self._labels_to_portals["AA"].get_single_connection

    @property
    def end_pos(self) -> DiscretePoint2:
        """The position for label `ZZ`"""
        return self._labels_to_portals["ZZ"].get_single_connection

    def tileAtPos(self, pos: DiscretePoint2) -> TileType:
        """Return the tile type at a position"""
        return self._maze[pos.y][pos.x]

    def findTimeBetweenPos(
        self,
        start_pos: Optional[DiscretePoint2] = None,
        end_pos: Optional[DiscretePoint2] = None,
        plutonian: bool = False,
    ) -> int:
        """
        Return the time to move between `start_pos` and `end_pos`

        if `start_pos` or `end_pos` is not provided, use the default
            (label `AA` or label `ZZ` respectively)
        pass `plutonian = True` to enable plutonian search
        """

        if start_pos is None:
            start_pos = self.start_pos
        if end_pos is None:
            end_pos = self.end_pos

        print(f"Finding path from {start_pos} to {end_pos} (plutonian={plutonian})")
        if self.tileAtPos(start_pos) not in [TileType.PASSAGE, TileType.PORTAL]:
            raise RuntimeError(
                f"start_pos ({start_pos}) is an invalid type: {self.tileAtPos(start_pos)}"
            )
        if self.tileAtPos(end_pos) not in [TileType.PASSAGE, TileType.PORTAL]:
            raise RuntimeError(
                f"end_pos ({end_pos}) is an invalid type: {self.tileAtPos(end_pos)}"
            )

        # Since this is part 1, we are relatively bounded on depth
        #   so just do a simple BFS
        #   turns out this works on part2 too
        best_times: dict[tuple[DiscretePoint2, int], int] = {}
        frontier: deque[tuple[DiscretePoint2, int, int]] = deque()
        frontier.append((start_pos, 0, 0))

        while len(frontier) > 0:
            this_pos, this_dist, this_depth = frontier.popleft()

            if this_depth < 0:
                # this was not explicitly disallowed in the instructions
                #   but apparently its a relevant condition
                continue

            if (this_pos, this_depth) in best_times:
                continue
            best_times[(this_pos, this_depth)] = this_dist

            if this_pos == end_pos and this_depth == 0:
                return this_dist

            # expand via portal
            if self.tileAtPos(this_pos) == TileType.PORTAL:
                portal = self._positions_to_portals[this_pos]

                if portal.inside_pos == this_pos and portal.outside_pos:
                    if plutonian:
                        # print(f"Using {portal.label} to go {portal.inside_pos} to {portal.outside_pos} {this_depth}+1 depth")
                        frontier.append(
                            (portal.outside_pos, this_dist + 1, this_depth + 1)
                        )
                    else:
                        frontier.append((portal.outside_pos, this_dist + 1, this_depth))
                elif portal.outside_pos == this_pos and portal.inside_pos:
                    if plutonian:
                        # print(f"Using {portal.label} to go {portal.outside_pos} to {portal.inside_pos} {this_depth}-1 depth")
                        frontier.append(
                            (portal.inside_pos, this_dist + 1, this_depth - 1)
                        )
                    else:
                        frontier.append((portal.inside_pos, this_dist + 1, this_depth))

            # expand via cartesian neighbors
            for new_pos in this_pos.cartesian_neighbors():
                if self.tileAtPos(new_pos) in [TileType.PASSAGE, TileType.PORTAL]:
                    frontier.append((new_pos, this_dist + 1, this_depth))

        raise RuntimeError("There was no path between start_pos and end_pos")

    def print(self) -> None:
        """Print the maze to the console"""
        for row in self._maze:
            print("".join(map(lambda x: x.render(), row)))


class Solution_2019_20(SolutionBase):
    """https://adventofcode.com/2019/day/20"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.maze = DonutMaze.fromLines(self.input_str_list(strip=False))

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return self.maze.findTimeBetweenPos()

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return self.maze.findTimeBetweenPos(plutonian=True)
