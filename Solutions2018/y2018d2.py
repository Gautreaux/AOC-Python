# from AOC_Lib.name import *

from collections import Counter

from AOC_Lib.npairs import allPairsGenerator

# sample variant for reading data from an input file, line by line


def y2018d2(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d2.txt"
    print("2018 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None

    twoCount = 0
    threeCount = 0

    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

            c = Counter(line)

            for i in [2, 3]:
                if len(list(filter(lambda x: x[1] == i, c.items()))) != 0:
                    if i == 2:
                        twoCount += 1
                    else:
                        threeCount += 1
        Part_1_Answer = twoCount * threeCount

        # part 2
        for x, y in allPairsGenerator(lineList):
            assert len(x) == len(y)
            diffs = 0
            dIDX = 0
            for i in range(len(x)):
                if x[i] != y[i]:
                    diffs += 1
                    dIDX = i
            if diffs == 1:
                Part_2_Answer = x[:dIDX] + x[dIDX + 1 :]

    return (Part_1_Answer, Part_2_Answer)
