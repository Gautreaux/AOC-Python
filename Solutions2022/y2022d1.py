# from AOC_Lib.name import *

def y2022d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2022/d1.txt"
    print("2022 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    elves = []

    running_total = 0

    for line in lineList:
        if line:
            i = int(line)
            running_total += i
        else:
            elves.append(running_total)
            running_total = 0
    if running_total:
        elves.append(running_total)

    Part_1_Answer = max(elves)

    elves.sort()

    Part_2_Answer = sum(elves[-3:])

    return (Part_1_Answer, Part_2_Answer)
