# from AOC_Lib.name import *

from collections import defaultdict, deque
from enum import IntEnum, unique


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


def y2019d20(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d20.txt"
    print("2019 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            # horrifically slow
            while line[-1] in ['\r', '\n']:
                line = line[:-1]
            lineList.append(line)
    

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

    my_maze = []
    portal_candidates = {}

    # read in the walls and paths
    for y_value, row in enumerate(lineList):
        maze_row = []
        for x_value, char in enumerate(row):
            if char == ".":
                maze_row.append(TileType.PASSAGE)
            elif char == "#":
                maze_row.append(TileType.WALL)
            elif char == " ":
                maze_row.append(TileType.WHITESPACE)
            elif ((ord(char) >= ord('A')) and (ord(char) <= ord('Z'))):
                portal_candidates[(x_value, y_value)] = char
                maze_row.append(TileType.WHITESPACE)
            else:
                raise RuntimeError(f"Unrecognized character: {char}")
        my_maze.append(maze_row)

    def getPassagePosition(x_1,y_1,x_2, y_2) -> tuple[int, int]:
        """get the passage position from the two letter positions"""
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

    # now match the portals
    matched_portals = defaultdict(list)

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

    # # And that concludes the reading in part
    # # display helper function
    # for row in my_maze:
    #     print("".join(map(lambda x: x.render(), row)))
    # # ===================

    # TODO - need to precompute components

    # build reverse map
    portal_to_label = {}
    for label, positions in matched_portals.items():
        for p in positions:
            portal_to_label[p] = label

    # now for the traversals, 
    #   simple BFS

    start_pos = matched_portals['AA'][0]
    goal_pos = matched_portals['ZZ'][0]

    best_times = {}

    frontier = deque()
    frontier.append((start_pos, 0))

    while len(frontier) > 0:
        this_pos, this_depth = frontier.popleft()


        if this_pos in best_times:
            continue
        best_times[this_pos] = this_depth

        if this_pos == goal_pos:
            break

        # print(f"Expanding {this_pos} from depth {this_depth}")
        # check portal expansion
        try:
            portal_label = portal_to_label[this_pos]
            # print(f"  This is a portal {portal_label} to ", end ="")
            for n in matched_portals[portal_label]:
                if n == this_pos:
                    continue
                frontier.append((n, this_depth + 1))
                print(f" {n} ", end ="")
            print("")
        except KeyError:
            pass

        # cartesian expansion
        this_x, this_y = this_pos
        for m_x, m_y in [(0,1),(1,0),(-1,0),(0,-1)]:
            new_x = this_x + m_x
            new_y = this_y + m_y

            if my_maze[new_y][new_x] in [TileType.PASSAGE, TileType.PORTAL]:
                frontier.append(((new_x, new_y), this_depth + 1))

    Part_1_Answer = best_times[goal_pos]

    return (Part_1_Answer, Part_2_Answer)