# from AOC_Lib.name import *

from copy import deepcopy

def y2017d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d5.txt"
    print("2017 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(int(line))
    
    # for multi line inputs
    steps = 0
    index = 0
    instrList = deepcopy(lineList)

    try:
        while True:
            instrList[index] += 1
            index += instrList[index] - 1
            steps += 1
    except IndexError:
        Part_1_Answer = steps

    steps = 0
    index = 0
    instrList = deepcopy(lineList)
    try:
        while True:
            jmp = instrList[index]
            instrList[index] += (1 if jmp < 3 else -1)
            index += jmp
            steps += 1
    except IndexError:
        Part_2_Answer = steps

    return (Part_1_Answer, Part_2_Answer)