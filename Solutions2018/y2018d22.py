# from AOC_Lib.name import *

from collections import namedtuple
from enum import Enum, unique
import functools
import sys

sys.setrecursionlimit(10000)

from AOC_Lib.pqueue import PQueue

@unique
class EquipmentType(Enum):
    NEITHER = 0,
    TORCH = 1,
    CLIMBING_GEAR = 2,


SearchState = namedtuple("SearchState", "time pos equipment")

@unique
class TileType(Enum):
    ROCKY = '.'
    WET = '='
    NARROW = '|'


class TileMap:
    
    def __init__(self, depth: int, target:tuple[int,int]) -> None:
        self._depth = depth
        self._target = target
        self._geologic_x_magic = 16807
        self._geologic_y_magic = 48271
        self._erosion_magic = 20183

    @functools.cache
    def getGeologicIndex(self, pos: tuple[int, int]) -> int:
        if pos == (0,0):
            return 0
        if pos == self._target:
            return 0
        if pos[1] == 0:
            return pos[0] * self._geologic_x_magic
        if pos[0] == 0:
            return pos[1] * self._geologic_y_magic
        return self.getErosionIndex((pos[0]-1, pos[1]))*self.getErosionIndex((pos[0],pos[1]-1))
    
    @functools.cache
    def getErosionIndex(self, pos: tuple[int, int]) -> int:
        return (self._depth + self.getGeologicIndex(pos)) % self._erosion_magic

    def getTileType(self, pos: tuple[int, int]) -> TileType:
        m = self.getErosionIndex(pos) % 3
        if m == 0:
            return TileType.ROCKY
        elif m == 1:
            return TileType.WET
        else:
            return TileType.NARROW

    def getRiskLevel(self, pos: tuple[int, int]) -> int:
        return self.getErosionIndex(pos) % 3


def y2018d22(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d22.txt"
    print("2018 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    depth = int(lineList[0].split(" ")[-1])
    target = tuple(map(int, lineList[1].split(" ")[-1].split(",")))

    tile_map = TileMap(depth, target)

    risk = 0

    for y in range(target[1]+1):
        for x in range(target[0]+1):
            risk += tile_map.getRiskLevel((x,y))

    Part_1_Answer = risk

    ## Part 2 

    def manhattanDistToTarget(pos: tuple[int, int])-> int:
        return sum(map(lambda x,y: abs(x-y), pos, target))

    def isValidState(s: SearchState) -> bool:
        p = s.pos

        if p[0] < 0 or p[1] < 0:
            return False
        
        e = s.equipment
        try:
            t = tile_map.getTileType(p)
        except RecursionError:
            print(f"recursion error while getting {p}")
            raise

        if t == TileType.NARROW:
            return e != EquipmentType.CLIMBING_GEAR
        elif t == TileType.WET:
            return e != EquipmentType.TORCH
        elif t == TileType.ROCKY:
            return e != EquipmentType.NEITHER

    pq = PQueue()
    pq.push(SearchState(0, (0,0), EquipmentType.TORCH), 0)

    visited = {}

    i = 0

    while len(pq) > 0:
        i += 1
        if i % 5000 == 0:
            print(f"Iteration {i}: remain {len(pq)}")

        this_state = pq.popMin()
        time = this_state.time
        pos = this_state.pos
        equipment = this_state.equipment

        # check visited
        if (pos,equipment) in visited:
            assert(time >= visited[(pos,equipment)])
            continue
        visited[(pos,equipment)] = time

        if Part_2_Answer is not None and time >= Part_2_Answer:
            continue

        # check goal
        if pos == target and equipment == EquipmentType.TORCH:
            print(f"Found new best time {time}, states remain: {len(pq)}")
            Part_2_Answer = time
            break # safe if your heuristic is ok (it is now)

        # generate successor states

        # in the current pos, change equipment
        for new_equip in EquipmentType:
            if new_equip == equipment:
                continue
            new_state = SearchState(time+7, pos, new_equip)
            if isValidState(new_state):
                pq.push(new_state, new_state.time + manhattanDistToTarget(new_state.pos))
        
        # move into a neighboring cell
        for new_state in [
            SearchState(time+1, (pos[0]-1, pos[1]), equipment),
            SearchState(time+1, (pos[0]+1, pos[1]), equipment),
            SearchState(time+1, (pos[0], pos[1]-1), equipment),
            SearchState(time+1, (pos[0], pos[1]+1), equipment),
        ]:
            if isValidState(new_state):
                pq.push(new_state, new_state.time + manhattanDistToTarget(new_state.pos))
    
    # print(Part_2_Answer)
    # assert(Part_2_Answer < 1104)
    # assert(Part_2_Answer < 1099)

    return (Part_1_Answer, Part_2_Answer)