# from AOC_Lib.name import *

from enum import IntEnum, unique
import itertools
from typing import Generator

from AOC_Lib.NeighborGenerator import neighborGeneratorFactory


@unique
class TileType(IntEnum):
    EMPTY = 0
    BUG = 1


ERIS_MAP_T = list[list[TileType]]

ERIS_RMAP_T = set[tuple[int, int, int]]


def getNextState(state: ERIS_MAP_T) -> ERIS_MAP_T:
    """Get the next state for this map"""
    ngf = neighborGeneratorFactory(4,4)

    new_map = [
        [0]*5,
        [0]*5,
        [0]*5,
        [0]*5,
        [0]*5,
    ]

    for y, row in enumerate(state):
        for x, c in enumerate(row):
            num_neighbor_bugs = sum(map(lambda x: 1 if state[x[1]][x[0]] else 0, ngf(x,y)))
            
            if c == TileType.BUG:
                if num_neighbor_bugs == 1:
                    new_map[y][x] = TileType.BUG
                else:
                    new_map[y][x] = TileType.EMPTY
            else:
                if num_neighbor_bugs == 1 or num_neighbor_bugs == 2:
                    new_map[y][x] = TileType.BUG
                else:
                    new_map[y][x] = TileType.EMPTY
    return new_map


def erisMapGenerator(start_map: ERIS_MAP_T) -> Generator[ERIS_MAP_T, None, None]:
    """Yield the start map and then consecutive maps, forever"""
    yield start_map
    current_map = start_map
    while True:
        current_map = getNextState(current_map)
        yield current_map


def hashErisMap(eris_map: ERIS_MAP_T) -> int:
    """Get a hash value for this map"""
    return hash(tuple(map(tuple, eris_map)))


def getBioDiversityScore(eris_map: ERIS_MAP_T) -> int:
    """Get the bio diversity score for the eris map"""
    score = 0

    for p, t in enumerate(itertools.chain.from_iterable(eris_map)):
        if t == TileType.BUG:
            score += (2 ** p)

    return score


def getPlutonianAdjacent(x_value:int, y_value: int, z_value:int) -> Generator[tuple[int, int, int], None, None]:

    assert(not (x_value == 2 and y_value == 2))

    # the non-recursive cases
    ngf = neighborGeneratorFactory(4,4)
    for new_x, new_y in ngf(x_value, y_value):
        if new_x == 2 and new_y == 2:
            continue
        yield (new_x, new_y, z_value)

    # the outer edge cases
    if x_value == 0:
        yield ((1, 2, z_value - 1))
    if x_value == 4:
        yield ((3, 2, z_value - 1))
    if y_value == 0:
        yield ((2, 1, z_value - 1))
    if y_value == 4:
        yield ((2, 3, z_value - 1))

    # the inner edge cases
    if x_value == 2 and y_value == 1:
        for i in range(5):
            yield ((i, 0, z_value + 1))
    if x_value == 2 and y_value == 3:
        for i in range(5):
            yield ((i, 4, z_value + 1))
    if y_value == 2 and x_value == 1:
        for i in range(5):
            yield ((0, i, z_value + 1))
    if y_value == 2 and x_value == 3:
        for i in range(5):
            yield ((4, i, z_value + 1))


def getNewPlutonianMap(current_map: ERIS_RMAP_T) -> ERIS_RMAP_T:
    """O(bad)"""

    assert(not any(map(lambda x: x[0] == 2 and x[1] == 2, current_map)))
    max_z = max(map(lambda x: x[2], current_map))
    min_z = min(map(lambda x: x[2], current_map))

    new_map = set()

    for z_layer in range(min_z - 1, max_z + 2):
        for x_value in range(5):
            for y_value in range(5):
                if x_value == 2 and y_value == 2:
                    continue

                num_neighbor_bugs = sum(
                    map(
                        lambda c: 1 if c in current_map else 0, 
                        getPlutonianAdjacent(x_value,y_value,z_layer)
                    )
                )

                if (x_value,y_value,z_layer) in current_map:
                    if num_neighbor_bugs == 1:
                        new_map.add((x_value,y_value,z_layer))
                else:
                    if num_neighbor_bugs == 1 or num_neighbor_bugs == 2:
                        new_map.add((x_value,y_value,z_layer))
    return new_map


def y2019d24(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d24.txt"
    print("2019 day 24:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    eris_map = []
    eris_r_map = set() # for part 2

    for line in lineList:
        assert(len(line) == 5)
        this_row = []
        for c in line:
            if c == '#':
                this_row.append(TileType.BUG)
                eris_r_map.add((len(this_row), len(eris_map), 0))
            elif c == ".":
                this_row.append(TileType.EMPTY)
            else:
                raise RuntimeError(f"Unrecognized character `{c}`")
        eris_map.append(this_row)

    assert(len(eris_map) == 5)

    seen_maps = set()

    for current_map in erisMapGenerator(eris_map):
        h = hashErisMap(current_map)
        if h in seen_maps:
            Part_1_Answer = getBioDiversityScore(current_map)
            break
        else:
            seen_maps.add(h)

    ##########
    # Part 2 #
    ##########

    assert(sum(1 for _ in getPlutonianAdjacent(0,0,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(1,0,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(2,0,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(3,0,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(4,0,0)) == 4)

    assert(sum(1 for _ in getPlutonianAdjacent(0,1,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(1,1,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(2,1,0)) == 8)
    assert(sum(1 for _ in getPlutonianAdjacent(3,1,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(4,1,0)) == 4)

    assert(sum(1 for _ in getPlutonianAdjacent(0,2,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(1,2,0)) == 8)
    # assert(sum(1 for _ in getPlutonianAdjacent(2,2,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(3,2,0)) == 8)
    assert(sum(1 for _ in getPlutonianAdjacent(4,2,0)) == 4)

    assert(sum(1 for _ in getPlutonianAdjacent(0,3,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(1,3,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(2,3,0)) == 8)
    assert(sum(1 for _ in getPlutonianAdjacent(3,3,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(4,3,0)) == 4)

    assert(sum(1 for _ in getPlutonianAdjacent(0,4,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(1,4,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(2,4,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(3,4,0)) == 4)
    assert(sum(1 for _ in getPlutonianAdjacent(4,4,0)) == 4)

    eris_r_map = {
        (4,0,0),
        (0,1,0),
        (3,1,0),
        (0,2,0),
        (3,2,0),
        (4,2,0),
        (2,3,0),
        (0,4,0),
    }

    for i in range(10):
        if i % 1 == 0:
            print(f"Minutes: {i}")

        eris_r_map = getNewPlutonianMap(eris_r_map)

    Part_2_Answer = len(eris_r_map)

    for z_layer in range(-5, 6):
        print("Depth {}:".format(z_layer))
        for y_value in range(4):
            for x_value in range(4):
                if (x_value, y_value, z_layer) in eris_r_map:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")
        print("")

    print("Part 2 guess: ", Part_2_Answer)
    assert(Part_2_Answer < 2012)
    assert(Part_2_Answer < 1932)

    return (Part_1_Answer, Part_2_Answer)