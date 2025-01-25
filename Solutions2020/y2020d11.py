# from AOC_Lib.name import *

from os import stat
from AOC_Lib.boundedInt import LockedInt
from copy import deepcopy


def getAllSurroundingGenerator(x, y, state):
    x = LockedInt(0, len(state[0]) - 1, value=x)
    y = LockedInt(0, len(state) - 1, value=y)

    transforms = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    yielded = set()
    yielded.add((x, y))

    for t in transforms:
        nx = (x + t[0]).asInt()
        ny = (y + t[1]).asInt()

        p = (nx, ny)
        if p not in yielded:
            yielded.add(p)
            yield p


sightCache = {}


def getAllSurroundingGeneratorPt2(x, y, state):
    inPos = (x, y)
    if inPos in sightCache:
        for p in sightCache[inPos]:
            yield p
        return

    # actually compute the sight line for this position
    thisPositions = []

    transforms = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    for t in transforms:
        nx = deepcopy(x)
        ny = deepcopy(y)
        lastPos = (nx, ny)
        while True:
            nx += t[0]
            ny += t[1]
            thisPos = (nx, ny)

            if nx < 0 or nx > len(state[0]) - 1:
                break
            if ny < 0 or ny > len(state) - 1:
                break

            k = state[ny][nx]
            if k == ".":
                continue
            else:
                assert k in ["L", "#"]
                thisPositions.append(thisPos)
                break
    sightCache[inPos] = thisPositions
    for p in thisPositions:
        yield p


def doRound(inState):
    rowList = []
    for oldY in range(len(inState)):
        thisRow = []
        for oldX in range(len(inState[oldY])):
            thisSeat = inState[oldY][oldX]
            if thisSeat == ".":
                thisRow.append(".")
            else:
                adjOccupied = 0
                for x, y in getAllSurroundingGenerator(oldX, oldY, inState):
                    # print(f"({x}, {y})")
                    if inState[y][x] == "#":
                        adjOccupied += 1
                if thisSeat == "L" and adjOccupied == 0:
                    thisRow.append("#")
                elif thisSeat == "#" and adjOccupied >= 4:
                    thisRow.append("L")
                else:
                    thisRow.append(thisSeat)
        rowList.append(thisRow)
    return rowList


def doRoundPt2(inState, doPrint=False):
    rowList = []
    for oldY in range(len(inState)):
        thisRow = []
        for oldX in range(len(inState[oldY])):
            thisSeat = inState[oldY][oldX]
            if thisSeat == ".":
                thisRow.append(".")
            else:
                adjOccupied = 0
                for x, y in getAllSurroundingGeneratorPt2(oldX, oldY, inState):
                    if doPrint:
                        print(f"({oldX}, {oldY}):({x}, {y}) ==> {inState[y][x]}")
                    if inState[y][x] == "#":
                        adjOccupied += 1
                if thisSeat == "L" and adjOccupied == 0:
                    thisRow.append("#")
                elif thisSeat == "#" and adjOccupied >= 5:
                    thisRow.append("L")
                else:
                    thisRow.append(thisSeat)
        rowList.append(thisRow)
    return rowList


def countAllSeats(inState):
    seatCount = 0
    for y in range(len(inState)):
        for x in range(len(inState[y])):
            if inState[y][x] == "#":
                seatCount += 1
    return seatCount


def printState(inState):
    for y in range(len(inState)):
        for x in range(len(inState[y])):
            print(inState[y][x], end="")
        print("")  # newline
    print("")


def y2020d11(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d11.txt"
    print("2020 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lastSeats = -1
    thisState = lineList

    # xx = 19
    # yy = 11
    # print(lineList[yy][xx])
    # for x,y in getAllSurroundingGeneratorPt2(xx, yy, lineList):
    #     print(f"({x}, {y}): {lineList[y][x]}")

    roundCounter = 0

    while True:
        newState = doRound(thisState)
        newcount = countAllSeats(newState)
        if newcount == lastSeats:
            Part_1_Answer = newcount
            break

        thisState = newState
        lastSeats = newcount

        roundCounter += 1
        if roundCounter % 5 == 0:
            print(f"Pt1 Round Counter on: {roundCounter}")

    lastSeats = -1
    thisState = lineList

    # Part_1_Answer = 2310
    roundCounter = 0

    # print(lineList[8])

    while True:

        if False:
            newState = doRoundPt2(thisState, True)
            newcount = countAllSeats(newState)

            printState(newState)
            if roundCounter == 1:
                break
        else:
            newState = doRoundPt2(thisState)
            newcount = countAllSeats(newState)

        if newcount == lastSeats:
            Part_2_Answer = newcount
            break

        thisState = newState
        lastSeats = newcount

        roundCounter += 1
        if roundCounter % 5 == 0:
            print(f"Pt2 Round Counter on: {roundCounter}")

    assert Part_2_Answer != 2198

    return (Part_1_Answer, Part_2_Answer)
