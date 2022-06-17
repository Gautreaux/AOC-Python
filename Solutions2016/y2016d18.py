# from AOC_Lib.name import *

import itertools
from typing import Generator

from AOC_Lib.SlidingWindow import sliding_window

SAFE = '.'
TRAP = '^'

_reduce = {
    (SAFE, SAFE, SAFE) : SAFE,
    (SAFE, SAFE, TRAP) : TRAP,
    (SAFE, TRAP, SAFE) : SAFE,
    (SAFE, TRAP, TRAP) : TRAP,
    (TRAP, SAFE, SAFE) : TRAP,
    (TRAP, SAFE, TRAP) : SAFE,
    (TRAP, TRAP, SAFE) : TRAP,
    (TRAP, TRAP, TRAP) : SAFE,
}

def getNextRow(in_row: str) -> str:
    """Get the next row of tiles"""
    new_row = itertools.chain(SAFE, in_row, SAFE)
    windows = sliding_window(new_row, n=3)
    return "".join(map(lambda x: _reduce[x], windows))


def generateRows(firstRow: str) -> Generator[str, None, None]:
    """Generate the rows, including the first row"""
    yield firstRow
    r = firstRow
    while True:
        r = getNextRow(r)
        yield r


def y2016d18(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d18.txt"
    print("2016 day 18:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)

    first_row = lineList[0]
    
    assert(len(set(first_row) ^ {SAFE, TRAP}) == 0)

    all_tiles = itertools.chain.from_iterable(
        itertools.islice(
            generateRows(first_row), 
            40,
        )
    )

    f = filter(lambda x: x == SAFE, all_tiles)

    Part_1_Answer = sum(1 for _ in f)

    all_tiles = itertools.chain.from_iterable(
        itertools.islice(
            generateRows(first_row), 
            400000,
        )
    )

    f = filter(lambda x: x == SAFE, all_tiles)

    Part_2_Answer = sum(1 for _ in f)

    return (Part_1_Answer, Part_2_Answer)