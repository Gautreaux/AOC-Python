# from AOC_Lib.name import *

from AOC_Lib.npairs import allPairsGenerator


def y2017d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d2.txt"
    print("2017 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for single line inputs
    for c in lineList[-1]:
        pass

    # for multi line inputs
    Part_1_Answer = 0
    Part_2_Answer = 0
    for line in lineList:
        line = line.replace("\t", ' ')
        # print(line)
        s = list(map(lambda x: int(x), line.split(" ")))
        Part_1_Answer += max(s) - min(s)

        for x,y in allPairsGenerator(s):
            if x % y == 0:
                Part_2_Answer += x//y
                break
            elif y % x == 0:
                Part_2_Answer += y//x
                break

    return (Part_1_Answer, Part_2_Answer)