# from AOC_Lib.name import *

from AOC_Lib.charSets import ALPHABET_LOWER
from collections import Counter

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

    # for multi line inputs 
    thisPassport = ""
    for line in lineList:
        if line == "":
            Part_1_Answer += getCount(thisPassport)
            thisPassport = ""
        else:
            thisPassport += line + " "

    # part 2
    i = -1
    charSet = Counter()
    lines = 0
    while i < len(lineList)-1:
        i += 1
        if lineList[i] == "":
            s = sum(map(lambda x: 0 if x[0] not in ALPHABET_LOWER else (1 if x[1] == lines else 0), charSet.items()))
            Part_2_Answer += s
            
            charSet = Counter()
            lines = 0
        else:
            charSet.update(lineList[i])
            lines += 1


    return (Part_1_Answer, Part_2_Answer)