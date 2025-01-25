# from AOC_Lib.name import *

import itertools
from typing import Generator


def generateCodes(first_code: int = 20151125) -> Generator[int, None, None]:
    """Generate the codes in order"""
    c = first_code

    while True:
        yield c
        c = (c * 252533) % (33554393)


def generateGridTiles() -> Generator[tuple[int, int], None, None]:
    """Generate the tiles in order"""
    for i in itertools.count(start=2):
        for j in range(1, i):
            r = i - j
            assert r >= 1
            assert j >= 1
            assert (r + j) == i
            yield (r, j)


def y2015d25(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d25.txt"
    print("2015 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    assert len(lineList) == 1

    s = lineList[-1].split(" ")

    row = int(s[-3][:-1])
    col = int(s[-1][:-1])

    rc_target = (row, col)

    last_sum = 0

    for tile, value in zip(generateGridTiles(), generateCodes()):
        if sum(tile) > last_sum:
            print(f"At {sum(tile)} of {sum(rc_target)}")
            last_sum = sum(tile) + 25

        if tile == rc_target:
            Part_1_Answer = value
            break

    return (Part_1_Answer, Part_2_Answer)
