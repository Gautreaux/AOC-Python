# from AOC_Lib.name import *

from math import lcm


def doReduction(diskList):
    if len(diskList) <= 1:
        return diskList[0]

    i = iter(diskList)

    combineDisk = next(i)

    # if i actually understood chinese remainder theorem
    #   this could probably be more efficient
    while True:
        try:
            sz0, off0 = next(i)
        except StopIteration:
            return combineDisk

        sz1, off1 = combineDisk

        newPeriod = lcm(sz0, sz1)

        def solutionGenerator():
            v = sz0 - off0
            while True:
                yield v
                v += sz0

        def isSolution(x):
            return ((x + off1) % sz1) == 0

        for sol in solutionGenerator():
            if isSolution(sol):
                smallestCommon = sol
                break

        newOff = newPeriod - smallestCommon

        combineDisk = (newPeriod, newOff)

        print(f"{(sz0, off0)} and {(sz1, off1)} --> {combineDisk}")


def y2016d15(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d15.txt"
    print("2016 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    diskList = []
    for line in lineList:
        l = line.split(" ")

        diskId = int(l[1][1:])

        nPos = int(l[3])
        offset = int(l[-1][:-1]) + diskId

        diskList.append((nPos, offset))

    # print(diskList)
    superDisk = doReduction(diskList)
    Part_1_Answer = superDisk[0] - superDisk[1]

    print(" ")
    superDisk = doReduction([superDisk, (11, len(diskList) + 1)])
    Part_2_Answer = superDisk[0] - superDisk[1]

    return (Part_1_Answer, Part_2_Answer)
