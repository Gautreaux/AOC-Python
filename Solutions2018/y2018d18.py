# from AOC_Lib.name import *

from enum import Enum
import functools

from AOC_Lib.ConwayBase import ConwayBase, ConwayCell_T, ConwayNeighbors_T

class CellType(Enum):
    OPEN = '.'
    TREES = '|'
    LUMBER_YARD = '#'


def nextState(cell: ConwayCell_T, neighbors: ConwayNeighbors_T) -> ConwayCell_T:
    if cell == CellType.OPEN:
        s = sum(1 for c in neighbors if c == CellType.TREES)
        if s >= 3:
            return CellType.TREES
        else:
            return CellType.OPEN
    elif cell == CellType.TREES:
        s = sum(1 for c in neighbors if c == CellType.LUMBER_YARD)
        if s >= 3:
            return CellType.LUMBER_YARD
        else:
            return CellType.TREES
    elif cell == CellType.LUMBER_YARD:
        m = map(
            lambda c: ((True, False) if c == CellType.LUMBER_YARD else(
                (False, True) if c == CellType.TREES else (False, False)
            )),
            neighbors
        )
        r = functools.reduce(
            lambda x,y: (x[0] or y[0], x[1] or y[1]),
            m
        )
        if all(r):
            return CellType.LUMBER_YARD
        else:
            return CellType.OPEN
    else:
        raise RuntimeError(f"Bad Value: {cell}")

def y2018d18(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d18.txt"
    print("2018 day 18:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    grid = []

    for line in lineList:
        new_row = []
        for cell in line:
            new_row.append(CellType(cell))
        assert(len(new_row) == 50)
        grid.append(new_row)

    assert(len(grid) == 50)

    conway = ConwayBase(grid, nextState, use_diagonals=True)

    conway.advance(10)

    num_trees = sum(conway.cMap(lambda x: 1 if x == CellType.TREES else 0))
    num_lumber = sum(conway.cMap(lambda x: 1 if x == CellType.LUMBER_YARD else 0))

    Part_1_Answer = num_trees * num_lumber

    # ========== part 2
    
    conway = ConwayBase(grid, nextState, use_diagonals=True)

    state_index: dict[tuple[CellType,...], int] = {}

    BIG_TARGET = 1000000000

    period = None

    for i in range(10000):
        if i % 25 == 0:
            print(f"i = {i}")
        conway.advance(1)
        t = tuple(conway.cMap())
        if t in state_index:
            print(f"Found first repeat from {state_index[t]} at {i}")
            start_repeat = state_index[t]
            next_repeat = i
            period = next_repeat - start_repeat
            break
        else:
            state_index[t] = i
    # BIG_TARGET = 740
    # start_repeat = 431
    # next_repeat = 459
    # period = next_repeat - start_repeat

    if period is None:
        raise RuntimeError("The lumberyard should be cyclical otherwise this problem is untenable")
    
    # figure out where the ending condition is
    m = (BIG_TARGET-1) % period

    print(f"Ends a modulo {m}")
    # print(f"  End should be 26 (corresponds to 446)")

    candidate = None

    for i in range(start_repeat, next_repeat):
        if i % period == m:
            assert(candidate is None)
            candidate = i

    assert(candidate is not None)
    print(f"Candidate resolved to: {candidate}")

    end_state = next(map(lambda x: x[0], filter(lambda x: x[1] == candidate, state_index.items())))
    
    num_trees = sum(map(lambda x: 1 if x == CellType.TREES else 0, end_state))
    num_lumber = sum(map(lambda x: 1 if x == CellType.LUMBER_YARD else 0, end_state))

    Part_2_Answer = num_trees * num_lumber

    # assert(Part_2_Answer > 202768)

    return (Part_1_Answer, Part_2_Answer)