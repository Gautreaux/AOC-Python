# from AOC_Lib.name import *

import itertools
from typing import Final


from AOC_Lib.HexGrid import (
    GRID_HORIZONTAL,
    HEX_STEP_TRANSLATIONS,
    HEX_TRANSFORMS,
    HexGrid,
    getAdjacentHexTiles,
)
from AOC_Lib.point import Point2

BLACK: Final = 1


def stepsGenerator(string):
    ew = ["e", "w"]
    charGen = iter(string)
    for c in charGen:
        if c in ew:
            yield c
        elif c == "n":
            c = next(charGen)
            assert c in ew
            if c == "e":
                yield "ne"
            else:
                yield "nw"
        elif c == "s":
            c = next(charGen)
            assert c in ew
            if c == "e":
                yield "se"
            else:
                yield "sw"
        else:
            raise RuntimeError(f"Unknown Char '{c}'")


def getPosForLine(line: str, start=(0, 0)) -> Point2:
    p = Point2(start)
    for step in stepsGenerator(line):
        p += HEX_TRANSFORMS[HEX_STEP_TRANSLATIONS[step]]
    return p


def y2020d24(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d24.txt"
    print("2020 day 24:")
    # print("DEBUGMODE ON")
    # inputPath = "Input2020/d24-sample.txt"

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    print(len(lineList))

    referenceTile = Point2(0, 0)
    theRoom = {}

    # DEBUG TESTING
    assert getPosForLine("nww") == Point2(-3, 1)
    assert getPosForLine("nwwswee") == Point2(0, 0)

    # for multi line inputs
    for line in lineList:
        thisTile = referenceTile
        for step in stepsGenerator(line):
            thisTile += HEX_TRANSFORMS[HEX_STEP_TRANSLATIONS[step]]
        # print(thisTile)
        if thisTile in theRoom:
            theRoom.pop(thisTile)
        else:
            theRoom[thisTile] = BLACK

    # for pos in theRoom.keys():
    #     print(theRoom[pos])

    Part_1_Answer = len(list(theRoom.keys()))

    # now for part 2

    for dayNum in range(100):
        newRoom = {}
        positions = set(
            itertools.chain(
                theRoom.keys(),
                *(
                    map(
                        lambda x: getAdjacentHexTiles(x, GRID_HORIZONTAL),
                        theRoom.keys(),
                    )
                ),
            )
        )
        # print(positions)

        for pos in positions:
            isBlack = pos in theRoom
            adjBlackCount = sum(
                map(
                    lambda x: 1 if x in theRoom else 0,
                    getAdjacentHexTiles(pos, GRID_HORIZONTAL),
                )
            )
            if isBlack is True:
                if adjBlackCount == 0 or adjBlackCount > 2:
                    # turn white
                    pass
                else:
                    # remain black:
                    newRoom[pos] = BLACK
            else:
                if adjBlackCount == 2:
                    # turn black
                    newRoom[pos] = BLACK
                else:
                    # remain white
                    pass

        # print(f"Day {dayNum+1}: {len(newRoom.keys())}")
        theRoom = newRoom

    Part_2_Answer = len(list(theRoom.keys()))

    assert Part_1_Answer != 169

    return (Part_1_Answer, Part_2_Answer)
