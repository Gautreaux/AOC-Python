# from AOC_Lib.name import *

# sample variant for reading data from an input file, line by line
from AOC_Lib.point import Point2
from AOC_Lib.point import Y_DOWN_2_TRANSFORMS as transforms
from AOC_Lib.boundedInt import LockedInt


def y2016d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d2.txt"
    print("2016 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None

    partialCode = ""
    partialCode2 = ""

    position = Point2(LockedInt(0,2,1), LockedInt(0,2,1))
    position2 = Point2(LockedInt(0,4,0), LockedInt(0,4,2))

    keypad = [[1,2,3],
              [4,5,6],
              [7,8,9]]

    N = None
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    keypad2 = [[N, N, 1, N, N],
                 [N, 2, 3, 4, N],
                 [5, 6, 7, 8, 9],
                 [N, A, B, C, N],
                 [N, N, D, N, N]]

    print(position)

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            for c in line:
                position += transforms[c]

                tempPos = position2 + transforms[c]
                if keypad2[tempPos.y.asInt()][tempPos.x.asInt()] != N:
                    position2 = tempPos
            partialCode += str(keypad[position.y.asInt()][position.x.asInt()])
            partialCode2 += str(keypad2[position2.y.asInt()][position2.x.asInt()])
    Part_1_Answer = partialCode
    Part_2_Answer = partialCode2
    return (Part_1_Answer, Part_2_Answer)

    
