# from AOC_Lib.name import *

from collections import defaultdict
from enum import IntEnum, unique

SPRING_X = 500
SPRING_Y = 0


@unique
class TileType(IntEnum):
    CLAY = 0
    UKN_SAND = 1
    DRAIN_SAND = 2
    TRAPPED_SAND = 3
    WET_TRAPPED_SAND = 4
    WET_DRAIN_SAND = 5

    def isWet(self) -> bool:
        return self == TileType.WET_DRAIN_SAND or self == TileType.WET_TRAPPED_SAND
    
    def wontDrain(self) -> bool:
        return self == TileType.CLAY or self == TileType.TRAPPED_SAND or self == TileType.WET_TRAPPED_SAND
    
    def render(self) -> str:
        if self == TileType.CLAY:
            return "#"
        elif self == TileType.WET_DRAIN_SAND:
            return "|"
        elif self == TileType.WET_TRAPPED_SAND:
            return "~"
        elif self == TileType.DRAIN_SAND:
            return ";"
        elif self == TileType.TRAPPED_SAND:
            return "-"
        elif self == TileType.UKN_SAND:
            return "?"
        else:
            raise RuntimeError(self)


def y2018d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d17.txt"
    print("2018 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # Sample Input
    # lineList = ["x=495, y=2..7",
    #             "y=7, x=495..501",
    #             "x=501, y=3..7",
    #             "x=498, y=2..4",
    #             "x=506, y=1..2",
    #             "x=498, y=10..13",
    #             "x=504, y=10..13",
    #             "y=13, x=498..504",
    # ]
    
    
    tiles = defaultdict(lambda: TileType.UKN_SAND)

    for line in lineList:
        lhs,rhs = line.split(", ")

        lhs_value = int(lhs[2:])
        rhs_r_start, rhs_r_end = rhs[2:].split("..")
        rhs_range = range(int(rhs_r_start), int(rhs_r_end) + 1)

        for v in rhs_range:
            if lhs[0] == 'x':
                assert rhs[0] == 'y'
                tiles[(lhs_value, v)] = TileType.CLAY
            else:
                assert(lhs[0] == 'y')
                assert(rhs[0] == 'x')
                tiles[(v, lhs_value)] = TileType.CLAY
    
    min_x = min(map(lambda x: x[0], tiles.keys()))
    max_x = max(map(lambda x: x[0], tiles.keys()))
    min_y = min(map(lambda x: x[1], tiles.keys()))
    max_y = max(map(lambda x: x[1], tiles.keys()))
    
    # for later validation that nothing went weird
    clay_checksum = len(tiles)
    dims_checksum = (min_x, max_x, min_y, max_y)

    print(f"X_range is {min_x} to {max_x}")
    print(f"Y_range is {min_y} to {max_y}")

    # setup some initial conditions
    for x in range(min_x-1, max_x + 2):
        tiles[(x, max_y+1)] = TileType.DRAIN_SAND
    for y in range(0, max_y+2):
        tiles[(min_x-1, y)] = TileType.DRAIN_SAND
        tiles[(max_x+1, y)] = TileType.DRAIN_SAND

    # now build a map of who drains and who doesn't
    for y in range(max_y, -1, -1):

        draining_tiles = [(min_x-1, y),(max_x+1, y)]
        
        # first the items that drain straight down
        for x in range(min_x, max_x + 1):
            p = (x,y)

            if tiles[p] != TileType.UKN_SAND:
                continue

            down_pos = (x,y+1)

            if tiles[down_pos] == TileType.DRAIN_SAND:
                tiles[p] = TileType.DRAIN_SAND
                draining_tiles.append(p)
        
        # now any spreading logic 
        while draining_tiles:
            this_p = draining_tiles.pop()

            if this_p[0] >= min_x:
                left_p = (this_p[0]-1, this_p[1])
                if tiles[left_p] == TileType.UKN_SAND:
                    tiles[left_p] = TileType.DRAIN_SAND
                    draining_tiles.append(left_p)
            if this_p[0] <= max_x:
                right_p = (this_p[0]+1, this_p[1])
                if tiles[right_p] == TileType.UKN_SAND:
                    tiles[right_p] = TileType.DRAIN_SAND
                    draining_tiles.append(right_p)
        
        # now for the trapped sand logic
        for x in range(min_x, max_x+1):
            p = (x, y)

            if tiles[p] != TileType.UKN_SAND:
                continue

            down_pos = (x,y+1)

            if tiles[down_pos].wontDrain():
                tiles[p] = TileType.TRAPPED_SAND

    for y in range(SPRING_Y, min_y):
        tiles[(SPRING_X, y)] = TileType.DRAIN_SAND
    
    print(f"Done Building drain map")

    # Now for the flood logic

    explore_frontier = [(SPRING_X, SPRING_Y)]

    while explore_frontier:
        p = explore_frontier.pop()

        if p[0] < min_x-1 or p[0] > max_x+1:
            continue

        if p[1] > max_y:
            continue

        t = tiles[p]
        if t == TileType.UKN_SAND:
            print(f"The tile {p} is unknown")
            assert(t != TileType.UKN_SAND)

        if t in [TileType.CLAY, TileType.WET_DRAIN_SAND, TileType.WET_TRAPPED_SAND]:
            continue
        
        if t == TileType.TRAPPED_SAND:
            tiles[p] = TileType.WET_TRAPPED_SAND
            explore_frontier.append((p[0]-1, p[1]))
            explore_frontier.append((p[0]+1, p[1]))
            explore_frontier.append((p[0], p[1]+1))
            continue
        
        assert(t == TileType.DRAIN_SAND)
        
        tiles[p] = TileType.WET_DRAIN_SAND
        down_p = (p[0],p[1]+1)
        explore_frontier.append(down_p)
        if tiles[down_p].wontDrain():
            # expand laterally
            explore_frontier.append((p[0]-1, p[1]))
            explore_frontier.append((p[0]+1, p[1]))

    # render 
    with open("tmp.txt",'w') as out_file:
        for y in range(0, max_y+2):
            r = []
            for x in range(min_x-1, max_x + 2):
                t = tiles[(x,y)]
                r.append(t.render())
            r.append("\n")
            out_file.write("".join(r))

    water_tiles_count = sum(1 for _ in filter(
        lambda x: x[1].isWet(),
        filter(
            lambda x: x[0][1] <= max_y and x[0][1] >= min_y,
            tiles.items()
        )
    ))
    Part_1_Answer = water_tiles_count

    if Part_1_Answer <= 30860:
        print("!!!!\nVALUE IS TOO LOW\n!!!!")
    if Part_1_Answer >= 355215:
        print("!!!!\nVALUE IS TOO HIGH\n!!!!")
        
    # validate
    num_clays = sum(1 for x in tiles.values() if x == TileType.CLAY)
    assert(num_clays == clay_checksum)
    assert(dims_checksum == (min_x, max_x, min_y, max_y))
    for y in range(0, max_y+1):
        assert(tiles[(min_x-1, y)].wontDrain() is False)
        assert(tiles[(min_x-1, y)].wontDrain() is False)

    # PART 2 Answer

    trapped_tiles_count = sum(1 for _ in filter(
        lambda x: x == TileType.WET_TRAPPED_SAND,
        tiles.values(),
    ))

    Part_2_Answer = trapped_tiles_count

    return (Part_1_Answer, Part_2_Answer)