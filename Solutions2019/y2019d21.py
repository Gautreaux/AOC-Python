# from AOC_Lib.name import *

from .IntcodeLib import IntcodeProgram, IntcodeRunner


def y2019d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d21.txt"
    print("2019 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    # this seems like a lot for right now

    return (Part_1_Answer, Part_2_Answer)