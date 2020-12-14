# from AOC_Lib.name import *

def y2017d1(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d1.txt"
    print("2017 day 1:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for single line inputs
    line = lineList[0]
    Part_1_Answer = 0
    Part_2_Answer = 0
    for i in range(len(line)):
        if line[i] == line[(i+1) % len(line)]:
            Part_1_Answer += int(line[i])
        if line[i] == line[(i + len(line)//2) % len(line)]:
            Part_2_Answer += int(line[i])
    return (Part_1_Answer, Part_2_Answer)