# from AOC_Lib.name import *

def getRowFromLine(line:str) -> int:
    assert(len(line) >= 7)

    rowFB = line[:7]
    rowC = list(map(lambda x: '1' if x == 'B' else '0', rowFB))
    
    rowB = ""

    for c in rowC:
        rowB += c

    return (int(rowB, 2))


def getColFromLine(line: str) -> int:
    assert(len(line) >= 3)

    rowFB = line[-3:]
    rowC = list(map(lambda x: '1' if x == 'R' else '0', rowFB))
    
    rowB = ""

    for c in rowC:
        rowB += c
    
    # print(rowB)

    return (int(rowB, 2))


def y2020d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d5.txt"
    print("2020 day 5:")

    Part_1_Answer = 0
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    idList = []

    for line in lineList:
        row = getRowFromLine(line)
        col = getColFromLine(line)

        seatId = row*8+col

        # print(f"{row}, {col}")

        if(seatId > Part_1_Answer):
            Part_1_Answer = seatId

        idList.append(seatId)

    idList.sort()

    for i in range(len(idList) -1):
        if idList[i] +1 != idList[i+1]:
            assert(Part_2_Answer is None)
            Part_2_Answer = idList[i]+1

    return (Part_1_Answer, Part_2_Answer)