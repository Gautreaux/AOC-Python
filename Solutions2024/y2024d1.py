# from AOC_Lib.name import *
from collections import Counter


def y2024d1(inputPath=None):
    if inputPath == None:
        inputPath = "Input2024/d1.txt"
    print("2024 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lhs = []
    rhs = []

    for line in lineList:
        l, r = line.split()
        lhs.append(int(l))
        rhs.append(int(r))

    lhs.sort()
    rhs.sort()
    distances = (abs(l - r) for l, r in zip(lhs, rhs))

    Part_1_Answer = sum(distances)

    c = Counter(rhs)

    Part_2_Answer = 0

    for l in lhs:
        Part_2_Answer += l * c.get(l, 0)

    return (Part_1_Answer, Part_2_Answer)
