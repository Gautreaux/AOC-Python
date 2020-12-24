
from typing import Any, Final, Generator

from AOC_Lib.point import Point2

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