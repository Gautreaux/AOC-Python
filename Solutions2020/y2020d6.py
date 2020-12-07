# from AOC_Lib.name import *

from AOC_Lib.charSets import ALPHABET_LOWER
from collections import Counter
from Solutions2020.y2020d4 import groupByEmptyLines

# per group
def getCount(ans:str)-> int:
    c = Counter(ans)
    return sum(map(lambda x: 1 if x[0] in ALPHABET_LOWER else 0, c))

def y2020d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d6.txt"
    print("2020 day 6:")

    Part_1_Answer = 0
    Part_2_Answer = 0
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)


    lineList.append("")

    lineGroups, linesQty = groupByEmptyLines(lineList)
    lineCount = len(lineGroups)

    for line, qty in zip(lineGroups, linesQty):
        Part_1_Answer += getCount(line)

        c = Counter(line)
        s = sum(map(lambda x: 0 if x[0] not in ALPHABET_LOWER else (1 if x[1] == qty else 0), c.items()))
        Part_2_Answer += s

    return (Part_1_Answer, Part_2_Answer)