# from AOC_Lib.name import *

from AOC_Lib.point import Point2, Y_UP_2_TRANSFORMS, Y_2_TRANSLATIONS
from AOC_Lib.boundedInt import BoundedInt

# TODO - there must be a better way


def getNextPosGenerator():
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0

    position = Point2(0, 0)
    direction = BoundedInt(4, value=1)

    yield position

    while True:
        position += Y_UP_2_TRANSFORMS[Y_2_TRANSLATIONS[direction.asInt()]]
        if position[0] < minX:
            minX = position[0]
            direction -= 1
        elif position[0] > maxX:
            maxX = position[0]
            direction -= 1
        elif position[1] < minY:
            minY = position[1]
            direction -= 1
        elif position[1] > maxY:
            maxY = position[1]
            direction -= 1
        yield position


def getSurroundingPositionGenerator(pos: Point2, memory):
    # yield all the points in memory around pos
    transforms = [
        Point2(-1, -1),
        Point2(0, -1),
        Point2(1, -1),
        Point2(-1, 0),
        Point2(1, 0),
        Point2(-1, 1),
        Point2(0, 1),
        Point2(1, 1),
    ]

    for t in transforms:
        np = pos + t
        if (np[0], np[1]) in memory:
            yield (np[0], np[1])


def getSurroundingGenerator(pos: Point2, memory) -> int:
    # yield all the values in memory around the pos
    for p in getSurroundingPositionGenerator(pos, memory):
        yield memory[(p[0], p[1])]


def y2017d3(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d3.txt"
    print("2017 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for single line inputs
    myInput = int(lineList[0])

    part1gen: Point2 = getNextPosGenerator()

    for _ in range(1, myInput):
        next(part1gen)
    p1pos = next(part1gen)

    Part_1_Answer = p1pos.manhattan()

    # part 2
    memory = {}

    part2gen = getNextPosGenerator()
    next(part2gen)  # skip the first 0,0
    memory[(0, 0)] = 1

    for pos in part2gen:
        thisValue = 0
        for adjValue in getSurroundingGenerator(pos, memory):
            thisValue += adjValue
        memory[(pos[0], pos[1])] = thisValue
        if thisValue > myInput:
            Part_2_Answer = thisValue
            break

    return (Part_1_Answer, Part_2_Answer)
