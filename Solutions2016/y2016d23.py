# from AOC_Lib.name import *

from Solutions2016.y2016d12 import runProgram


def y2016d23(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d23.txt"
    print("2016 day 23:")

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

    Part_1_Answer = runProgram(instructionSet, {"a": 7})["a"]
    Part_2_Answer = runProgram(instructionSet, {"a": 12})["a"]

    assert Part_2_Answer > 7716

    return (Part_1_Answer, Part_2_Answer)
