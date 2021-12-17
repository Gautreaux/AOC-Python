# from AOC_Lib.name import *

def y2021d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d12.txt"
    print("2021 day 12:")

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

    return (Part_1_Answer, Part_2_Answer)