# from AOC_Lib.name import *

# sample variant for single line inputs
from AOC_Lib.npairs import allPairsGenerator


def y2018d11(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d11.txt"
    print("2018 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        line = f.readline().strip()
    serialNumber = int(line)

    GRID_SIZE = 300

    grid = [None]*GRID_SIZE
    for i in range(GRID_SIZE):
        grid[i] = [0]*GRID_SIZE

    # build grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rackID = x *10
            powerLevel = rackID * y
            powerLevel += serialNumber
            powerLevel *= rackID
            
            hundredsDigit = (powerLevel % 1000) // 100
            grid[y][x] = hundredsDigit - 5

    # scan grid
    maxPower = 0
    maxIndex = (0,0)
    trans = [(0,0), (1,0), (2,0),
         (0,1), (1,1), (2,1),
         (0,2), (1,2), (2,2)]
    for y in range(GRID_SIZE - 2):
        for x in range(GRID_SIZE - 2) :
            partial = 0
            for t in trans:
                partial += grid[y+t[1]][x+t[0]]
            if partial > maxPower:
                maxPower = partial
                maxIndex = (x+1,y+1)

    # not 11,2?

    Part_1_Answer = maxIndex
    return (Part_1_Answer, Part_2_Answer)
