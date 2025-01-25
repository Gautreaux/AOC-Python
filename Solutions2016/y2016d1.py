# from AOC_Lib.name import *

# sample variant for single line inputs
from AOC_Lib.point import Point2, Y_2_TRANSLATIONS
from AOC_Lib.point import Y_UP_2_TRANSFORMS as transforms
from AOC_Lib.boundedInt import BoundedInt


def y2016d1(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d1.txt"
    print("2016 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        line = f.readline().strip()

    # TODO - this should probably be a generic class
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    direction = BoundedInt(4, value=NORTH)
    pos = Point2(0, 0)

    tokens = line.replace(" ", "").split(",")

    part2Set = set()
    part2Set.add(pos)

    # iterate the tokens
    for t in tokens:
        if t[0] == "R":
            direction += 1
        elif t[0] == "L":
            direction -= 1
        else:
            raise ValueError(t[0])

        tt = transforms[Y_2_TRANSLATIONS[direction]]

        for _ in range(int(t[1:])):
            pos += tt
            if Part_2_Answer is None and pos not in part2Set:
                part2Set.add(pos)
            elif Part_2_Answer is None and pos in part2Set:
                Part_2_Answer = abs(pos.x) + abs(pos.y)

    Part_1_Answer = abs(pos.x) + abs(pos.y)

    return (Part_1_Answer, Part_2_Answer)
