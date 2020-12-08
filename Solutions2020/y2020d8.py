# from AOC_Lib.name import *

import re

REGEX_STRING = "([a-z]{3}) ([+-][0-9]*)"

def runTrial(instrSet):
    accumulator = 0
    visitSet = set()
    nextInstr = 0
    try:
        while nextInstr not in visitSet:
            visitSet.add(nextInstr)

            # if nextInstr < 0 or nextInstr >= len(instrSet):
            #     raise IndexError()

            r = instrSet[nextInstr]
            if r[0] == 'acc':
                accumulator += int(r[1])
                nextInstr += 1
            elif r[0] == 'jmp':
                nextInstr += int(r[1])
            elif r[0] == 'nop':
                nextInstr += 1
            else:
                raise ValueError(r[0])
        return accumulator
    except IndexError:
        return (accumulator,) # force it to be tuple

def y2020d8(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d8.txt"
    print("2020 day 8:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    regexList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

            x = re.search(REGEX_STRING, line)
            assert(x is not None)
            regexList.append((x.group(1), x.group(2)))


    Part_1_Answer = runTrial(regexList)

    def inverseInstr(i):
        if regexList[i][0] == 'nop':
            regexList[i] = ('jmp', regexList[i][1])
        else:
            regexList[i] = ('nop', regexList[i][1])

    for i in range(len(regexList)):
        if regexList[i][0] == 'acc':
            continue

        inverseInstr(i)
        k = runTrial(regexList)
        if (type(k) == tuple):
            assert(Part_2_Answer == None)
            Part_2_Answer = k[0]
        inverseInstr(i)



    return (Part_1_Answer, Part_2_Answer)