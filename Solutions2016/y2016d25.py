# from AOC_Lib.name import *

import itertools

from Solutions2016.y2016d12 import runProgram


def y2016d25(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d25.txt"
    print("2016 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    instructionSet = []

    for line in lineList:
        l = line.split(" ")

        for i in [1, 2]:
            try:
                l[i] = int(l[i])
            except:
                pass
        instructionSet.append(l)
    # # TODO - refactor assemb-bunny into a library
    # for i in itertools.count(i):
    #     m = {'a': i}
    #     print()
    #     runProgram(instructionSet, memory=m)
    #     print("")

    return (Part_1_Answer, Part_2_Answer)
