# from AOC_Lib.name import *

from collections import deque
from enum import Enum, unique
from typing import Generator, Iterator, Optional


Pos_T = tuple[int, int]

@unique
class TileType(Enum):
    WALL = '#'
    OPEN = '.'


class Amphipod:

    def __init__(self, pos: Pos_T, a_type: str) -> None:
        self._pos = pos
        self._a_type = a_type
    
    def __str__(self) -> str:
        return self.a_type

    @property
    def pos(self) -> Pos_T:
        """Return the current pos"""
        return self._pos

    @property
    def a_type(self) -> Pos_T:
        """Return the type"""
        return self._a_type

    def desiredRoom(self) -> int:
        """Return the X coordinate of the desired room"""
        return {
            'a':3,
            'b':5,
            'c':7,
            'd':9
        }[self.a_type]

def computePairwiseDistance(valid_positions: set[Pos_T]) -> dict[Pos_T, dict[Pos_T, int]]:
    """Compute and Cache all pairwise distances"""

    transforms = [(-1,0), (1,0), (0,-1), (0,1)]
    to_return = {}

    for start_p in valid_positions:
        cache = {}
        q = deque()
        q.append((start_p, 0))

        while len(q) > 0:
            pos, dist = q.popleft()

            if pos in cache:
                assert(cache[pos] <= dist)
                continue
            cache[pos] = dist

            for t in transforms:
                np = (t[0] + pos[0], t[1] + pos[1])
                if np in cache:
                    continue
                elif np not in valid_positions:
                    continue
                else:
                    q.append((np, dist+1))
        to_return[start_p] = cache
    return to_return


class AmphipodsOrganizer:
    OPEN_TILES: set[Pos_T] = set([
        (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1),
                      (3,2),        (5,2),        (7,2),        (9,2),
                      (3,3),        (5,3),        (7,3),        (9,3),
    ])

    # CACHE of number of steps between distances
    DIST_CACHE: dict[Pos_T, dict[Pos_T, int]] = computePairwiseDistance(OPEN_TILES)

    def __init__(self, pods) -> None:
        self.amphipods: list[Amphipod] = pods

    @classmethod
    def fromInput(cls, lines: Iterator[str]) -> 'AmphipodsOrganizer':
        """Parse and construct based on the input"""

        pods = []

        for y,line in enumerate(lines):
            for x,cell in enumerate(line):
                if cell in "ABCD":
                    pods.append(Amphipod((x,y), cell))
                elif cell == '.':
                    assert((x,y) in cls.OPEN_TILES)
                elif cell == '#':
                    assert((x,y) not in cls.OPEN_TILES)

        ao = cls(pods)
        return ao
    
    # placeholders
    @property
    def min_x(self) -> int:
        return 0

    @property
    def max_x(self) -> int:
        return 12

    @property
    def min_y(self) -> int:
        return 0
    
    @property
    def max_y(self) -> int:
        return 4

    @classmethod
    def getTile(cls, xy: Pos_T) -> TileType:
        """Get the tile at the coordinates"""
        if xy in cls.OPEN_TILES:
            return TileType.OPEN
        else:
            return TileType.WALL

    @classmethod
    def generateTiles(cls, start_xy: Pos_T, end_xy: Pos_T) -> Generator[Pos_T, None, None]:
        """Generate the tiles on the patch from `start_xy` to `end_xy`"""

        if start_xy == end_xy: 
            return
        
        t_xy = start_xy

        while t_xy[1] < 1:
            t_xy = (t_xy[0], t_xy[1] + 1)
            yield t_xy
            if t_xy == end_xy:
                return
        while t_xy[0] != end_xy[0]:
            t_xy = (t_xy[0] + (1 if t_xy[0] < end_xy[0] else -1), t_xy[1])
            yield t_xy
            if t_xy == end_xy:
                return
        while t_xy[1] > end_xy[1]:
            t_xy = (t_xy[0], t_xy[1]-1)
            yield t_xy
            if t_xy == end_xy:
                return
        assert(False)
        

    @classmethod
    def isDirectlyOutsideRoom(cls, xy: Pos_T) -> bool:
        """Return True iff this position is directly outside a room"""
        if xy in [(3,1), (5,1), (7,1), (9,1)]:
            return False
        return True

    @classmethod
    def isInRoom(cls, xy: Pos_T) -> bool:
        """Return True iff this position is inside a room"""
        if xy[1] <= 1:
            return False
        elif cls.getTile(xy) == TileType.WALL:
            return False
        else:
            return True

    @classmethod
    def isDestinationRoom(cls, xy: Pos_T, a: Amphipod) -> bool:
        """Return True iff this position is in the destination room for A"""
        if not cls.isInRoom(xy):
            return False
        return xy[0] == a.desiredRoom()
        

    def canStopHere(self, xy: Pos_T, a: Amphipod) -> bool:
        """Return True iff the Amphipod `a` can stop at position `xy`"""
        if self.isDirectlyOutsideRoom(xy):
            return False
        elif not self.isInRoom(xy):
            return True
        elif not self.isDestinationRoom(xy, a):
            return False
        
        # need to check who else is in the room
        f = filter(lambda a: a.pos[0] == xy[0], self.amphipods)

        in_room = list(f)
        if len(in_room) == 2:
            return False
        elif len(in_room) == 1:
            if in_room[0].a_type == a.a_type:
                return True
            else:
                return False
        else:
            return False
    
    def distMoveToPos(self, xy: Pos_T, a: Amphipod) -> Optional[int]:
        """Return int distance the Amphipod `a` can move to position `pos`
            None otherwise
        """
        if not self.canStopHere(xy, a):
            return False
        # check that all tiles are clear
        for t in self.generateTiles(a.pos, xy):
            for a in self.amphipods:
                if a.pos == t:
                    return False
        return True

    def draw(self) -> None:
        """Draw the current state to the console"""
        pod_locations = {a.pos:a for a in self.amphipods}

        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                if (x,y) in pod_locations:
                    print(pod_locations[(x,y)], end="")
                    continue
                else:
                    print(self.getTile((x,y)).value, end="")
            
            print("", end='\n')



def y2021d23(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d23.txt"
    print("2021 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            # line = line.strip()
            lineList.append(line)
    
    
    ao = AmphipodsOrganizer.fromInput(lineList)

    ao.draw()
    
    return (Part_1_Answer, Part_2_Answer)