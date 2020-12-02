# from AOC_Lib.name import *

def isTriangle(a, b, c) -> bool:
    if a + b <= c:
        return False
    if b + c <= a:
        return False
    if a +c <= b:
        return False
    return True

def y2016d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d3.txt"
    print("2016 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None

    linesList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            while "  " in line:
                line = line.replace("  ", " ")
            linesList.append(list(map(lambda x: int(x), line.split(" "))))

    Part_1_Answer = sum(map(lambda x: 1 if isTriangle(*x) else 0, linesList))

    Part_2_Answer = 0

    assert(len(linesList) % 3 == 0)
    for i in range(len(linesList)//3):
        for j in range(3):
            if isTriangle(linesList[i*3][j], linesList[i*3+1][j], linesList[i*3+2][j]):
                Part_2_Answer += 1
        
        
    return (Part_1_Answer, Part_2_Answer)