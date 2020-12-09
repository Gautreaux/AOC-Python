# from AOC_Lib.name import *

def preambleOK(intList, index):
    for i in range(index -25, index):
        for j in range(i+1, index):
            if intList[i] + intList[j] == intList[index]:
                return True
    return False

def findContiguous(intList, index):
    target = intList[index]
    for i in range(len(intList)):
        for j in range(2, len(intList) - i):
            s = intList[i:i+j]
            if sum(s) == target:
                assert(len(s) >= 2)
                return min(s) + max(s)

def y2020d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d9.txt"
    print("2020 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(int(line))
    
    for i in range(25, len(lineList)):
        if preambleOK(lineList, i):
            pass
        else:
            if Part_1_Answer is None:
                Part_1_Answer = lineList[i]
                Part_2_Answer = findContiguous(lineList, i)
                break


    return (Part_1_Answer, Part_2_Answer)