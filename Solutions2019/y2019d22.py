# from AOC_Lib.name import *

def y2019d22(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d22.txt"
    print("2019 day 22:")

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