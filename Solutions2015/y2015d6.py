# from AOC_Lib.name import *

import itertools

TOGGLE = 0
TURN_ON = 1
TURN_OFF = 2

def y2015d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d6.txt"
    print("2015 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    def parseTuple(tupleStr):
        return tuple(map(int, tupleStr.split(',')))

    instrList = []
    for line in lineList:
        s = line.split(" ")

        if s[0] == "toggle":
            instrList.append((
                TOGGLE,
                parseTuple(s[1]),
                parseTuple(s[-1]),
            ))
        else:
            instrList.append((
                TURN_OFF if s[1] == "off" else TURN_ON,
                parseTuple(s[2]),
                parseTuple(s[-1]),
            ))

    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    grid2 = [[0 for _ in range(1000)] for _ in range(1000)]

    for instr, left, right in instrList:
        for x in range(left[0], right[0]+1):
            for y in range(left[1], right[1]+1):
                if instr == TURN_ON:
                    grid[y][x] = 1
                    grid2[y][x] += 1
                elif instr == TURN_OFF:
                    grid[y][x] = 0
                    grid2[y][x] = max(grid2[y][x] - 1, 0)
                elif instr == TOGGLE:
                    grid[y][x] = 1 if grid[y][x] == 0 else 0
                    grid2[y][x] += 2

    Part_1_Answer = sum(itertools.chain.from_iterable(grid))
    Part_2_Answer = sum(itertools.chain.from_iterable(grid2))

    return (Part_1_Answer, Part_2_Answer)