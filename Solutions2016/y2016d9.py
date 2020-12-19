# from AOC_Lib.name import *

from os import pardir


def getLenTimesFromGenerator(gen):
    expansionInternals = []
    while True:
        # no try-catch so that exception goes up
        c = next(gen)
        if c == ")":
            break
        else:
            expansionInternals.append(c)
    expansionInternals = "".join(expansionInternals)
    s = expansionInternals.split("x")
    assert(len(s) == 2)
    return tuple(map(int, s))

def doExpansion(line):
    def characterGenerator():
        for c in line:
            yield c

    charGen = characterGenerator()

    newLine = []
    while True:
        try:
            n = next(charGen)
        except StopIteration:
            # no more characters in the line
            return "".join(newLine)
        if n != "(": # ) <- to make the formatter happy
            newLine.append(n)
            continue
        
        # time to process an expansion
        numChars, numTimes = getLenTimesFromGenerator(charGen)
        expansionStr = []
        while len(expansionStr) < numChars:
            expansionStr.append(next(charGen))
        expansionStr = "".join(expansionStr)
        for _ in range(numTimes):
            newLine.append(expansionStr)

def limitedGenerator(length, baseGenerator):
    for _ in range(length):
        yield next(baseGenerator)


def getExpandedLen(charGen) -> int:
    partial = 0
    for c in charGen:
        if c != '(':  # ) <= to make the formatter happy
            partial += 1
            continue
        
        # do the actual expansion
        numChars, numTimes = getLenTimesFromGenerator(charGen)
        newGen = limitedGenerator(numChars, charGen)
        i = getExpandedLen(newGen)
        partial += i * numTimes
    return partial


def y2016d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d9.txt"
    print("2016 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    Part_1_Answer = len(doExpansion(lineList[-1]))
    def lineGen():
        for c in lineList[-1]:
            yield c
    Part_2_Answer = getExpandedLen(lineGen())

    return (Part_1_Answer, Part_2_Answer)