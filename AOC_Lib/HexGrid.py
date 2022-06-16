
from collections import namedtuple
from typing import Any, Final, Generator, Iterable

from AOC_Lib.pqueue import PQueue, heapq
from AOC_Lib.point import Point2

# type for hex pos
HEX_POS_T = tuple[int, int]

# TODO - proper Enums

GRID_HORIZONTAL : Final = 0
GRID_VERTICAL : Final = 1

HEX_STEP_N  : Final = 1
HEX_STEP_E  : Final = 2
HEX_STEP_S  : Final = 3
HEX_STEP_W  : Final = 4
HEX_STEP_NE : Final = 5
HEX_STEP_SE : Final = 6
HEX_STEP_SW : Final = 7
HEX_STEP_NW : Final = 8

HEX_STEP_TRANSLATIONS : Final = {
    'N'  : HEX_STEP_N,
    "n"  : HEX_STEP_N,
    "S"  : HEX_STEP_S,
    "s"  : HEX_STEP_S,
    "E"  : HEX_STEP_E,
    "e"  : HEX_STEP_E,
    "W"  : HEX_STEP_W,
    "w"  : HEX_STEP_W,
    "NE" : HEX_STEP_NE,
    "ne" : HEX_STEP_NE,
    "NW" : HEX_STEP_NW,
    "nw" : HEX_STEP_NW,
    "SE" : HEX_STEP_SE,
    "se" : HEX_STEP_SE,
    "SW" : HEX_STEP_SW,
    "sw" : HEX_STEP_SW
}

_HEX_STEPS_HORIZONTAL : Final = [
        HEX_STEP_E, HEX_STEP_W, 
        HEX_STEP_NE, HEX_STEP_NW, 
        HEX_STEP_SE, HEX_STEP_SW]

_HEX_STEPS_VERTICAL : Final = [
        HEX_STEP_N, HEX_STEP_S,
        HEX_STEP_NE, HEX_STEP_NW, 
        HEX_STEP_SE, HEX_STEP_SW
]

HEX_TRANSFORMS : Final = {
    HEX_STEP_N : Point2(0,2),
    HEX_STEP_S : Point2(0,-2),
    HEX_STEP_E : Point2(2,0),
    HEX_STEP_W : Point2(-2,0),
    HEX_STEP_NE : Point2(1,1),
    HEX_STEP_NW : Point2(-1,1),
    HEX_STEP_SE : Point2(1,-1),
    HEX_STEP_SW : Point2(-1,-1)
}

def getAdjacentHexTiles(position : Point2, gridOrientation : int) -> Generator[Point2, None, None]:
    assert(gridOrientation in [GRID_HORIZONTAL, GRID_VERTICAL])
    l = (_HEX_STEPS_HORIZONTAL if gridOrientation == GRID_HORIZONTAL else _HEX_STEPS_VERTICAL)
    for step in l:
        yield position + HEX_TRANSFORMS[step]


_SearchState = namedtuple("_SearchState", "pos dist")

def inferGridOrientation(steps: Iterable[str]) -> int:
    """Infer the grid orientation given step iterables
        returns either `GRID_VERTICAL` or `GRID_HORIZONTAL`
    """
    s = set(map(lambda x: HEX_STEP_TRANSLATIONS[x], steps))
    
    s_vertical = set(_HEX_STEPS_VERTICAL)
    s_horizontal = set(_HEX_STEPS_HORIZONTAL)

    is_vert = (len(s ^ s_vertical) == 0)
    is_horizontal = (len(s ^ s_horizontal) == 0)

    if is_vert and is_horizontal:
        # I guess this isn't strictly an error
        raise RuntimeError(f"Could not uniquely determine orientation")
    elif not is_vert and not is_horizontal:
        raise RuntimeError(f"Was neither horizontal nor vertical")
    elif is_vert:
        return GRID_VERTICAL
    else:
        return GRID_HORIZONTAL


def getAdjacentTiles(pos: HEX_POS_T, grid_orientation: int) -> Generator[HEX_POS_T, None, None]:
    """Get all tiles adjacent to the pos"""
    assert(grid_orientation in [GRID_HORIZONTAL, GRID_VERTICAL])
    n = (_HEX_STEPS_HORIZONTAL if (grid_orientation == GRID_HORIZONTAL) else _HEX_STEPS_VERTICAL)

    for t in map(lambda x: HEX_TRANSFORMS[x], n):
        yield (pos[0]+t[0], pos[1]+t[1])


def getAdjacentTiles_Vertical(pos: HEX_POS_T) -> Generator[HEX_POS_T, None, None]:
    """Get all tiles adjacent to the pos, for vertical grids"""
    return getAdjacentTiles(pos, GRID_VERTICAL)


def getAdjacentTiles_Horizontal(pos: HEX_POS_T) -> Generator[HEX_POS_T, None, None]:
    """Get all tiles adjacent to the pos, for horizontal grids"""
    return getAdjacentTiles(pos, GRID_HORIZONTAL)


def manhattanHexDist(pos_a: HEX_POS_T, pos_b: HEX_POS_T = (0,0)) -> int:
    """Get the manhattan dist between the tiles"""
    return (abs(pos_a[0] - pos_b[0]), abs(pos_a[1] - pos_b[1]))

def computeHexDistance(start_pos: HEX_POS_T, grid_dir: int, end_pos: HEX_POS_T = (0,0)) -> int:
    """Compute the minimum distance from `start_pos` to `end_pos`
        Assumes that the grid is infinite and complete (there are no holes/ blocked tiles)
    """
    # There is probably a more efficient way given the nature of the grid structure
    #   i.e. get to x/y 0 and then its a straight shot from there
    #   but trying to support having holes/blocks in the future
    if start_pos == end_pos:
        return 0

    pq = PQueue()
    pq.push(_SearchState(start_pos, 0), 0)

    visited: set[HEX_POS_T] = set()

    while len(pq) > 0:
        m: _SearchState = pq.popMin()

        if m.pos == end_pos:
            return m.dist

        if m in visited:
            continue
        visited.add(m.pos)

        # Generate Adjacent
        for a in getAdjacentTiles(m.pos, grid_dir):
            if a in visited:
                continue
            # Honestly, IDK why this gives the correct answer but whatever
            pq.push(_SearchState(a, m.dist+1), manhattanHexDist(a, end_pos))

    raise RuntimeError(f"No path from {start_pos} to {end_pos} could be found")


class HexGrid():
    def __init__(self, direction : int) -> None:
        assert(direction in [GRID_HORIZONTAL, GRID_VERTICAL])
        self.dir = direction
        self.tiles = {}

    def isValidKey(self, key: Point2) -> bool:
        try:
            assert((key[0] + key[1]) % 2 == 0)
            return True
        except Exception:
            return False

    def getNextKey(self, key : Point2, stepDirection : int) -> Point2:
        if self.dir == GRID_HORIZONTAL:
            assert(stepDirection in _HEX_STEPS_HORIZONTAL)
        else:
            assert(stepDirection in _HEX_STEPS_VERTICAL)
        return  key + HEX_TRANSFORMS[stepDirection]

    def getAdjacentTiles(self, key : Point2) -> Generator[Point2, None, None]:
        t = (_HEX_STEPS_HORIZONTAL if self.dir == GRID_HORIZONTAL else _HEX_STEPS_VERTICAL)

    def __setitem__(self, key : Point2, value : Any) -> Any:
        self.tiles[key] = value

    def __getitem__(self, key : Point2) -> Any:
        return self.tiles[key]

    def iterKeys(self) -> Generator[Any, None, None]:
        for k in self.tiles:
            yield k

    def remove(self, key : Point2) -> None:
        if key in self:
            self.tiles.pop(key)
        else:
            raise KeyError(key)

    def __contains__(self, key : Point2) -> bool:
        assert(self.isValidKey(key))
        return key in self.tiles