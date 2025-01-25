# from AOC_Lib.name import *


def y2020d10(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d10.txt"
    print("2020 day 10:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(int(line))

    myJolts = 3 + max(lineList)
    reduxVoltage = {}
    lineList.append(myJolts)
    lineList.append(0)
    lineList.sort()

    for i in range(len(lineList) - 1):
        r = lineList[i + 1] - lineList[i]
        if r not in [1, 3]:
            Warning(f"Suspect illegal R: {r}")
        if r not in reduxVoltage:
            reduxVoltage[r] = 1
        else:
            reduxVoltage[r] += 1
    Part_1_Answer = reduxVoltage[1] * reduxVoltage[3]

    # print(lineList)
    # print(reduxVoltage)

    # guess what a wrong answer is
    assert Part_1_Answer != 1809

    searchCache = {}
    searchCache[myJolts] = 1

    def resolveChain(startingIndex) -> int:
        k = lineList[startingIndex]
        if k in searchCache:
            return searchCache[k]

        d = 0
        for i in range(1, 4):
            try:
                if lineList[startingIndex + i] - k <= 3:
                    d += resolveChain(startingIndex + i)
            except IndexError:
                break

        searchCache[k] = d
        return d

    Part_2_Answer = resolveChain(0)

    return (Part_1_Answer, Part_2_Answer)
