# from AOC_Lib.name import *

def y2021d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d2.txt"
    print("2021 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    splits = []

    for line in lineList:
        x,y = line.split()
        splits.append((x, int(y)))

    hoz_pos = 0
    depth = 0

    # for part 2
    hoz_pos_2 = 0
    depth_2 = 0
    aim_2 = 0

    for instr, amt in splits:
        if instr == "forward":
            hoz_pos += amt
            hoz_pos_2 += amt
            depth_2 += aim_2 * amt
        elif instr == "up":
            depth -= amt
            aim_2 -= amt
        elif instr == "down":
            depth += amt
            aim_2 += amt
        else:
            raise ValueError(f"Illegal Instruction: {instr}")

    Part_1_Answer = hoz_pos * depth
    Part_2_Answer = hoz_pos_2 * depth_2

    return (Part_1_Answer, Part_2_Answer)