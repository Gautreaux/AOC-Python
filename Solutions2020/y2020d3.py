# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line

from AOC_Lib.boundedInt import BoundedInt


def slopeGenerator(xBound, xStep, yStep):
    x = BoundedInt(xBound)
    y = 0

    while True:
        yield (x.asInt(),y)
        x += xStep
        y += yStep

# part 2
def checkSlope(lineList, xStep, yStep):
    treeCount = 0
    try:
        for x,y in slopeGenerator(len(lineList[0]), xStep, yStep):
            if lineList[y][x]  == '#':
                treeCount += 1
    except IndexError:
        # Error occurs when the y value gets too large and drop out of the grid
        pass
    return treeCount

def y2020d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d3.txt"
    print("2020 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None

    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]

    treesCount = []

    for s in slopes:
        treesCount.append(checkSlope(lineList, *s))

        #change made after submitted
        if s == (3,1):
            Part_1_Answer = treesCount[-1]
    
    count = 1
    for t in treesCount:
        count  *= t
    Part_2_Answer = count
        
    return (Part_1_Answer, Part_2_Answer)
