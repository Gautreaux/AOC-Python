# from AOC_Lib.name import *

from collections import defaultdict, deque, namedtuple
from enum import IntEnum, unique


Pos_T = tuple[int, int]

PortalConnection_T = namedtuple("PortalConnection_T", "label outside_pos inside_pos")

@unique
class TileType(IntEnum):
    """The types of tiles"""
    PASSAGE = 0,
    WALL = 1,
    PORTAL = 2,
    WHITESPACE = 3,

    def render(self) -> str:
        if self.value == TileType.PASSAGE:
            return "."
        elif self.value == TileType.WALL:
            return "#"
        elif self.value == TileType.PORTAL:
            return "P"
        elif self.value == TileType.WHITESPACE:
            return " "


class DonutMaze:
    
    def __init__(self, maze:list[list[TileType]], portal_labels:dict[str, PortalConnection_T]) -> None:
        self._maze = maze
        self._labels_to_portals = portal_labels
        self._positions_to_portals = self._getPositionsToPortals()

    @classmethod
    def fromLines(cls, lineList: list[str]) -> 'DonutMaze':
        """Build an return an object from the line list"""
        # assert that the maze "starts at 2,2"
        assert(lineList[0][0] == " ")
        assert(lineList[1][0] == " ")
        assert(lineList[0][1] == " ")
        assert(lineList[1][1] == " ")
        assert(lineList[0][2] == " ")
        assert(lineList[1][2] == " ")
        assert(lineList[2][0] == " ")
        assert(lineList[2][1] == " ")
        assert(lineList[2][2] == "#")

        my_maze: list[list[TileType]] = []
        portal_candidates = {}

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
                elif ((ord(char) >= ord('A')) and (ord(char) <= ord('Z'))):
                    portal_candidates[(x_value, y_value)] = char
                    maze_row.append(TileType.WHITESPACE)
                else:
                    raise RuntimeError(f"Unrecognized character: {char}")
            my_maze.append(maze_row)

        # local helper function
        def getPassagePosition(x_1,y_1,x_2, y_2) -> Pos_T:
            """get the passage position from the two letter positions
                For the two positions of the letters,
                    return the position of the adjacent PASSAGE 
            """
            if y_1 == y_2:
                # horizontal case
                candidate_x_1 = min(x_1, x_2) - 1
                candidate_x_2 = max(x_1, x_2) + 1 # candidate_1 + 2?
                candidate_y_1 = y_1
                candidate_y_2 = y_1
            else:
                # vertical case
                candidate_x_1 = x_1
                candidate_x_2 = x_1
                candidate_y_1 = min(y_1, y_2) - 1
                candidate_y_2 = max(y_1, y_2) + 1
            
            for x,y in [(candidate_x_1, candidate_y_1), (candidate_x_2, candidate_y_2)]:
                try:
                    if x < 0 or y < 0:
                        continue
                    # print(f"Checking {x},{y} -> ", my_maze[y][x])
                    if my_maze[y][x] == TileType.PASSAGE:
                        return (x,y)
                except IndexError:
                    pass
            raise RuntimeError("No neighboring position was a passage")

        # mapping of portal label to position
        matched_portals = defaultdict(list)
        
        # now we want to find and update all passages with their tile type
        while portal_candidates:
                (this_x, this_y), this_letter = next(iter(portal_candidates.items()))

                num_matches = 0

                for other_x, other_y in [(this_x + 1, this_y), (this_x - 1, this_y), (this_x, this_y + 1), (this_x, this_y - 1)]:
                    try:
                        other_letter = portal_candidates[(other_x, other_y)]
                    except KeyError:
                        continue
                    
                    if other_x > this_x:
                        portal_name = f"{this_letter}{other_letter}"
                    elif other_x < this_x:
                        portal_name = f"{other_letter}{this_letter}"
                    elif other_y > this_y:
                        portal_name = f"{this_letter}{other_letter}"
                    else:
                        portal_name = f"{other_letter}{this_letter}"
                    # print("NAME: {} at {},{}".format(portal_name, this_x, this_y))
                    portal_pos = getPassagePosition(this_x, this_y, other_x, other_y)
                    matched_portals[portal_name].append(portal_pos)
                    num_matches += 1
                    my_maze[portal_pos[1]][portal_pos[0]] = TileType.PORTAL
                    portal_candidates.pop((this_x, this_y))
                    portal_candidates.pop((other_x, other_y))
                if num_matches == 0:
                    raise RuntimeError(f"This {(this_x, this_y)} does not have another candidate nearby")
                if num_matches > 1:
                    raise RuntimeError(f"This {(this_x, this_y)} does not multiple candidate nearby")
        
        # check that all the portals have exactly two candidates in their named pair
        for k,v in matched_portals.items():
            if k in ['ZZ', 'AA']:
                assert(len(v) == 1)
                continue
            if len(v) != 2:
                print(f"Key {k} got only portal {v} ")
            assert(len(v) == 2)

        fixed_portals = {}

        maze_w = len(my_maze[0])
        maze_h = len(my_maze)
        for label, positions in matched_portals.items():
            first_pos = positions[0]
            first_pos_is_outside = False

            does_x_imply_outside = first_pos[0] < 4 or (first_pos[0] + 4) >= maze_w
            does_y_imply_outside = first_pos[1] < 4 or (first_pos[1] + 4) >= maze_h

            first_pos_is_outside =  does_x_imply_outside or does_y_imply_outside

            if len(positions) == 1:
                assert(label in ['AA', 'ZZ'])
                assert(first_pos_is_outside)
                positions.append(None)
            else:
                assert(len(positions) == 2)
            
            if first_pos_is_outside:
                f_portal = PortalConnection_T(
                    label=label,
                    outside_pos=positions[0],
                    inside_pos=positions[1],
                )
            else:
                f_portal = PortalConnection_T(
                    label=label,
                    outside_pos=positions[1],
                    inside_pos=positions[0],
                )

            fixed_portals[label] = f_portal

        s = cls(my_maze, fixed_portals)
        return s

    def _getPositionsToPortals(self) -> dict[Pos_T, PortalConnection_T]:
        """Use the portal labels to positions map to get a positions to portals map"""
        to_return = {}
        for portal in self._labels_to_portals.values():
            if portal.inside_pos:
                assert(portal.inside_pos not in to_return)
                to_return[portal.inside_pos] = portal
            if portal.outside_pos:
                assert(portal.outside_pos not in to_return)
                to_return[portal.outside_pos] = portal
        return to_return
    
    @property
    def start_pos(self) -> Pos_T:
        """The position for label `AA`"""
        p = self._labels_to_portals['AA']
        if p.outside_pos is None:
            return p.inside_pos
        elif p.inside_pos is None:
            return p.outside_pos
        else:
            raise RuntimeError(f"Bad format for position: {p}")
    
    @property
    def end_pos(self) -> Pos_T:
        """The position for label `ZZ`"""
        p = self._labels_to_portals['ZZ']
        if p.outside_pos is None:
            return p.inside_pos
        elif p.inside_pos is None:
            return p.outside_pos
        else:
            raise RuntimeError(f"Bad format for position: {p}")

    def tileAtPos(self, pos: Pos_T) -> TileType:
        """Return the tile type at a position"""
        return self._maze[pos[1]][pos[0]]

    def findTimeBetweenPos(self, start_pos: Pos_T, end_pos: Pos_T, plutonian: bool = False) -> int:
        """Return the time to move between `start_pos` and `end_pos`"""

        print(f"Finding path from {start_pos} to {end_pos}")
        if self.tileAtPos(start_pos) not in [TileType.PASSAGE, TileType.PORTAL]:
            raise RuntimeError(f"start_pos ({start_pos}) is an invalid type: {self.tileAtPos(start_pos)}")
        if self.tileAtPos(end_pos) not in [TileType.PASSAGE, TileType.PORTAL]:
            raise RuntimeError(f"end_pos ({end_pos}) is an invalid type: {self.tileAtPos(end_pos)}")

        # Since this is part 1, we are relatively bounded on depth
        #   so just do a simple BFS
        #   turns out this works on part2 too
        best_times = {}
        frontier = deque()
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
                        frontier.append((portal.outside_pos, this_dist + 1, this_depth + 1))
                    else:
                        frontier.append((portal.outside_pos, this_dist + 1, this_depth))
                elif portal.outside_pos == this_pos and portal.inside_pos:
                    if plutonian:
                        # print(f"Using {portal.label} to go {portal.outside_pos} to {portal.inside_pos} {this_depth}-1 depth")
                        frontier.append((portal.inside_pos, this_dist + 1, this_depth - 1))
                    else:
                        frontier.append((portal.inside_pos, this_dist + 1, this_depth))

            # expand via cartesian neighbors
            this_x, this_y = this_pos
            for m_x, m_y in [(0,1),(1,0),(-1,0),(0,-1)]:
                new_x = this_x + m_x
                new_y = this_y + m_y

                if self.tileAtPos((new_x, new_y)) in [TileType.PASSAGE, TileType.PORTAL]:
                    frontier.append(((new_x, new_y), this_dist + 1, this_depth))

        raise RuntimeError("There was no path between start_pos and end_pos")

    def print(self) -> None:
        """Print the maze to the console"""
        for row in self._maze:
            print("".join(map(lambda x: x.render(), row)))


def y2019d20(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d20.txt"
    print("2019 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            lineList.append(line)
    
    maze = DonutMaze.fromLines(lineList)

    Part_1_Answer = maze.findTimeBetweenPos(
        start_pos=maze.start_pos,
        end_pos=maze.end_pos,
    )
    Part_2_Answer = maze.findTimeBetweenPos(
        start_pos=maze.start_pos,
        end_pos=maze.end_pos,
        plutonian=True,
    )

    print(f"Part 2 guess: {Part_2_Answer}")
    assert(Part_2_Answer > 3642)

    return (Part_1_Answer, Part_2_Answer)
