# from AOC_Lib.name import *

from types import BuiltinFunctionType


def y2020d15(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d15.txt"
    print("2020 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    inputList = list(map(int, lineList[-1].split(",")))

    print(inputList)

    spokenCache = {}
    lastNum = None
    isFirstTime = False

    turnCtr = 1

    # testing a theory about cyclic nature
    # zeroIndexes = []

    def speakNumber(number, turn) -> bool:
        # if number == 0:
        #     zeroIndexes.append(turn)
        # print(number)
        if number in spokenCache:
            last = spokenCache[number][0]
            spokenCache[number] = (turn, last)
            return (False, number)
        else:
            spokenCache[number] = (turn, None)
            return (True, number)

    def numDiff(number) -> int:
        i = spokenCache[number]
        return i[0] - i[1]

    for startNum in inputList:
        isFirstTime, lastNum = speakNumber(startNum, turnCtr)
        turnCtr += 1

    while turnCtr <= 2020:
        # speak a number
        if isFirstTime:
            isFirstTime, lastNum = speakNumber(0, turnCtr)
        else:
            n = numDiff(lastNum)
            isFirstTime, lastNum = speakNumber(n, turnCtr)
        turnCtr += 1

    Part_1_Answer = lastNum

    while turnCtr <= 30000000:
        if isFirstTime:
            isFirstTime, lastNum = speakNumber(0, turnCtr)
        else:
            n = numDiff(lastNum)
            isFirstTime, lastNum = speakNumber(n, turnCtr)
        turnCtr += 1

        if turnCtr % 1000000 == 0:
            print(f"turnCtr on {turnCtr}")

    Part_2_Answer = lastNum

    # print(zeroIndexes)

    return (Part_1_Answer, Part_2_Answer)
