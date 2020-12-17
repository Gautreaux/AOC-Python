# from AOC_Lib.name import *

import itertools
from copy import deepcopy
from typing import Dict, Generator, Tuple

ACTIVE = 1
INACTIVE = 0

# a tuple of one or more ints
TYPE_POSITION = Tuple[int, ...]
TYPE_STATE = Dict[TYPE_POSITION, int]

def generateSurroundingStates(position : TYPE_POSITION) -> Generator[TYPE_POSITION, None, None]:
    """Dimension unaware generate all neighbors of the position"""
    transforms = (-1,0,1)
    packed = [transforms]*len(position) # need to transform for each dimension
    allZeros = tuple(([0]*len(position))) # number of zeros equal to dimension size
    for permutation in itertools.product(*packed):
        if permutation == allZeros:
            continue
        else:
            yield tuple(map(lambda x,y: x+y, position, permutation))


def safeGetPosition(state : TYPE_STATE, position : TYPE_POSITION) -> int:
    """Get position, defaulting to INACTIVE if not present"""
    try:
        return state[position]
    except KeyError:
        return INACTIVE

def getSurroundingSum(state : TYPE_STATE, position : TYPE_POSITION) -> int:
    """Get the sum of all states surrounding the position"""
    return sum(map(lambda t: safeGetPosition(state, t), generateSurroundingStates(position)))

def getDimMinMax(state, dim : int) -> Tuple[int, int]:
    """Get the tuple(min, max) for the dimension"""
    l = list(map(lambda x: x[dim], state.keys()))
    return (min(l), max(l))

def genAllStatePositions(state : TYPE_STATE) -> Generator[TYPE_POSITION, None, None]:
    """Generate all possible positions from the given state"""
    dims = []
    nDims = len(list(state.keys())[0])
    for i in range(nDims):
        dims.append(getDimMinMax(state, i))
    
    valuesInDimension = []
    for dim in dims:
        valuesInDimension.append(list(range(dim[0]-1, dim[1]+2)))

    for p in itertools.product(*valuesInDimension):
        yield p

def runBoot(inState : TYPE_STATE) -> int:
    '''run the 6-cycle boot sequence for this state'''
    oldState = deepcopy(inState)
    for _ in range(6):
        newState = {}
        for position in genAllStatePositions(oldState):
            s = getSurroundingSum(oldState, position)
            nowValue = safeGetPosition(oldState, position)
            if nowValue == ACTIVE:
                if s in [2,3]:
                    newState[position] = ACTIVE
            else:
                if s == 3:
                    newState[position] = ACTIVE
        oldState = newState
    return sum(map(lambda x: 1 if x == ACTIVE else 0, oldState.values()))


def y2020d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d17.txt"
    print("2020 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # debugging
    # lineList = [".#.",
    #             "..#",
    #             "###"]

    conwayCube = {}
    conwayHyperCube = {}

    # for multi line inputs
    for y in range(len(lineList)):
        for x in range(len(lineList[y])):
            conwayCube[(x,y,0)] = (ACTIVE if lineList[y][x] == '#' else INACTIVE)
            conwayHyperCube[(x,y,0,0)] = (ACTIVE if lineList[y][x] == '#' else INACTIVE)

    # for t in generateSurroundingStates(4,1,0):
    #     print(t)

    # print(getSurroundingSum(myState, 0,0,0))
    # print(getSurroundingSum(myState, 1,4,0))    


    Part_1_Answer = runBoot(conwayCube)
    Part_2_Answer = runBoot(conwayHyperCube)

    assert(Part_1_Answer != 88)

    return (Part_1_Answer, Part_2_Answer)