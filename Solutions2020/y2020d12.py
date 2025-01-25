# from AOC_Lib.name import *

from AOC_Lib.boundedInt import BoundedInt
from AOC_Lib.point import *


def y2020d12(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d12.txt"
    print("2020 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # lineList = ["F10", "N3", "F7", "R90", "F11"]

    pos = Point2(0, 0)
    dir = BoundedInt(4, value=1)

    for line in lineList:
        i = line[0]
        j = int(line[1:])

        if i in ["N", "S", "E", "W"]:
            t = Y_UP_2_TRANSFORMS[Y_2_TRANSLATIONS[i]]
            pos += t * j
        elif i == "F":
            t = Y_UP_2_TRANSFORMS[Y_2_TRANSLATIONS[dir.asInt()]]
            pos += t * j
        elif i in ["L", "R"]:
            assert j % 90 == 0
            dir += (1 if i == "R" else -1) * (j // 90)
        else:
            raise ValueError(f"Illegal arg: {i}")

    Part_1_Answer = abs(pos[0]) + abs(pos[1])
    assert Part_1_Answer != 1982

    waypointPos = Point2(10, 1)
    shipPos = Point2(0, 0)

    for line in lineList:
        i = line[0]
        j = int(line[1:])

        if i in ["N", "S", "E", "W"]:
            t = Y_UP_2_TRANSFORMS[Y_2_TRANSLATIONS[i]]
            waypointPos += t * j
        elif i == "F":
            shipPos += waypointPos * j
        elif i == "L":
            while j >= 90:
                waypointPos = Point2(-waypointPos[1], waypointPos[0])
                j -= 90
        elif i == "R":
            while j >= 90:
                waypointPos = Point2(waypointPos[1], -waypointPos[0])
                j -= 90
        else:
            raise ValueError(f"Illegal arg: {i}")
        # print(f"{shipPos} {waypointPos}")

    Part_2_Answer = abs(shipPos[0]) + abs(shipPos[1])

    return (Part_1_Answer, Part_2_Answer)
